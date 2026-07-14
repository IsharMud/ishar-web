"""WebSocket consumer that proxies to a telnet MUD server."""
import asyncio
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from . import tracker
from .models import WebLoginToken


logger = logging.getLogger(__name__)

# Application close codes, so the browser can tell a *bridge* problem (retry
# with backoff, the game or bridge may be mid-deploy) from the game cleanly
# ending the session (a quit — don't fight it with an auto-reconnect loop).
# 4000-4999 is the private-use range of RFC 6455.
CLOSE_BRIDGE_FAILURE = 4502

# The WAIT_ACCOUNT_NAME prompt the game prints when it is ready for a login
# (src/server/output.c, send_prompt_other). Auto-login waits for it because
# input sent while the game is still in its pre-login states (ident/proxy
# lookups) is silently discarded — and minting on the prompt means none of
# the token's 90 s TTL is spent on that latency.
ACCOUNT_PROMPT = "please enter your account email"

# Telnet protocol constants.
IAC = 255    # Interpret As Command
DONT = 254
DO = 253
WONT = 252
WILL = 251
SB = 250     # Subnegotiation Begin
SE = 240     # Subnegotiation End

# Telnet options.
OPT_ECHO = 1
OPT_SGA = 3       # Suppress Go Ahead
OPT_TTYPE = 24    # Terminal Type
OPT_NAWS = 31     # Negotiate About Window Size
OPT_GMCP = 201    # Generic MUD Communication Protocol


class TelnetConsumer(AsyncWebsocketConsumer):
    """Proxy WebSocket connections to the MUD telnet server."""

    async def connect(self):
        self._reader = None
        self._writer = None
        self._read_task = None
        self._server_echo = False
        # Holds telnet bytes that arrived mid-sequence so a command or GMCP
        # subnegotiation split across socket reads is reassembled, not lost.
        self._inbuf = bytearray()
        # Latest window size reported by the browser (cols, rows); used to
        # answer the server's DO NAWS with the real terminal size.
        self._naws = None
        # Auto-login (#85 / ishar-mud#1773): a portal-authenticated player is
        # logged in by this consumer writing `webauth <token>` into the telnet
        # stream when the game shows its account prompt. The token is minted
        # here and never sent to the browser. AuthMiddlewareStack has already
        # resolved scope["user"] by this point.
        user = self.scope.get("user")
        account_id = (
            getattr(user, "account_id", None)
            if user is not None and user.is_authenticated
            else None
        )
        # States: account id set = waiting for the account prompt;
        # None = guest, already sent, or minting failed — leave manual login.
        self._autologin_account_id = account_id
        self._prompt_tail = ""

        # Accept before dialing the game: a close code sent on a never-accepted
        # socket surfaces in the browser as a bare handshake failure (1006),
        # which would be indistinguishable from a network drop.
        await self.accept()

        host = getattr(settings, "MUD_HOST", "localhost")
        port = getattr(settings, "MUD_PORT", 23)

        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=10,
            )
        except (ConnectionRefusedError, OSError, asyncio.TimeoutError) as exc:
            logger.error(
                "Failed to connect to MUD at %s:%s: %s", host, port, exc
            )
            await self.close(code=CLOSE_BRIDGE_FAILURE)
            return

        tracker.register(self)

        # Read from the MUD in the background.
        self._read_task = asyncio.create_task(self._read_telnet())

    async def disconnect(self, code):
        tracker.unregister(self)
        if self._read_task:
            self._read_task.cancel()
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception:
                pass

    async def receive(self, text_data=None, bytes_data=None):
        """Forward user input from WebSocket to telnet."""
        if bytes_data:
            # Binary frames carry raw telnet data (e.g. NAWS updates). Cache
            # the reported size — even before the telnet side is up, since the
            # browser sends its first NAWS the moment the socket opens — so a
            # later server DO NAWS gets the real terminal size.
            self._cache_naws(bytes_data)

        if not self._writer or self._writer.is_closing():
            return

        if bytes_data:
            self._writer.write(bytes_data)
        elif text_data:
            self._writer.write(text_data.encode("utf-8", errors="replace"))

        try:
            await self._writer.drain()
        except (ConnectionError, OSError):
            await self.close(code=CLOSE_BRIDGE_FAILURE)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _cache_naws(self, frame):
        """Remember the window size from a browser NAWS subnegotiation.

        The client only sends one kind of binary frame — ``IAC SB NAWS w1 w0
        h1 h0 IAC SE`` — so a strict shape check is enough. Anything else is
        ignored (and still forwarded verbatim by the caller).
        """
        if (
            len(frame) == 9
            and frame[0] == IAC and frame[1] == SB and frame[2] == OPT_NAWS
            and frame[7] == IAC and frame[8] == SE
        ):
            cols = (frame[3] << 8) | frame[4]
            rows = (frame[5] << 8) | frame[6]
            if 0 < cols < 1024 and 0 < rows < 1024:
                self._naws = (cols, rows)

    async def _maybe_autologin(self, display_data):
        """Send ``webauth <token>`` once the game shows its account prompt.

        The prompt is watched for in the displayable stream (with a small
        carry-over tail so a prompt split across socket reads still matches).
        On the first sighting, mint a single-use 90-second token for the
        authenticated account and answer the prompt from here — the token
        never reaches the browser. Any failure just leaves the player at the
        normal manual prompt.
        """
        text = self._prompt_tail + display_data.decode(
            "utf-8", errors="replace"
        ).lower()
        if ACCOUNT_PROMPT not in text:
            self._prompt_tail = text[-(len(ACCOUNT_PROMPT) - 1):]
            return

        account_id = self._autologin_account_id
        self._autologin_account_id = None  # one attempt per connection
        self._prompt_tail = ""

        try:
            token = await database_sync_to_async(WebLoginToken.mint)(
                account_id
            )
        except Exception as exc:
            # E.g. the game-side migration hasn't run yet. Manual login works.
            logger.warning(
                "Auto-login mint failed for account %s: %s", account_id, exc
            )
            return

        if self._writer and not self._writer.is_closing():
            self._writer.write(b"webauth " + token.encode("ascii") + b"\r\n")
            try:
                await self._writer.drain()
            except (ConnectionError, OSError):
                await self.close(code=CLOSE_BRIDGE_FAILURE)

    async def _read_telnet(self):
        """Continuously read from the MUD and forward to the WebSocket."""
        try:
            while True:
                data = await self._reader.read(4096)
                if not data:
                    # The game ended the session (quit, kick, or shutdown):
                    # a clean close, not a bridge failure.
                    await self.close(code=1000)
                    return

                self._inbuf.extend(data)
                display_data, responses, echo_changed, gmcp_messages = (
                    self._process_telnet()
                )

                # Send any telnet negotiation replies.
                if responses and self._writer and not self._writer.is_closing():
                    self._writer.write(responses)
                    try:
                        await self._writer.drain()
                    except (ConnectionError, OSError):
                        await self.close()
                        return

                # Notify the client if the server ECHO state changed
                # (used to toggle local echo and password masking).
                if echo_changed is True:
                    await self.send(text_data="\x00ECHO_ON")
                elif echo_changed is False:
                    await self.send(text_data="\x00ECHO_OFF")

                # Forward GMCP out-of-band data on a dedicated channel so the
                # browser HUD can parse it without polluting the terminal text
                # stream. Payload is "Package.Message {json}".
                for message in gmcp_messages:
                    await self.send(text_data="\x00GMCP " + message)

                # Forward displayable text to the browser.
                if display_data:
                    await self.send(
                        text_data=display_data.decode(
                            "utf-8", errors="replace"
                        )
                    )
                    # Auto-login: when the game reaches its account prompt,
                    # mint a token and answer for the authenticated player.
                    if self._autologin_account_id is not None:
                        await self._maybe_autologin(display_data)
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            logger.error("Telnet read error: %s", exc)
            await self.close(code=CLOSE_BRIDGE_FAILURE)

    def _process_telnet(self):
        """Parse buffered telnet data from ``self._inbuf``.

        Consumes as many complete telnet sequences as possible and leaves any
        trailing partial sequence in ``self._inbuf`` for the next read, so a
        large GMCP subnegotiation split across socket reads is reassembled
        rather than dropped.

        Returns ``(display_bytes, response_bytes, echo_changed,
        gmcp_messages)`` where *echo_changed* is True/False if the server ECHO
        state toggled (else None) and *gmcp_messages* is a list of decoded
        GMCP payload strings ("Package.Message {json}").
        """
        data = self._inbuf
        output = bytearray()
        responses = bytearray()
        gmcp_messages = []
        echo_changed = None
        i = 0
        consumed = 0
        length = len(data)

        while i < length:
            byte = data[i]

            if byte != IAC:
                output.append(byte)
                i += 1
                consumed = i
                continue

            # IAC at end of buffer – incomplete, wait for more data.
            if i + 1 >= length:
                break

            next_byte = data[i + 1]

            # Escaped 0xFF.
            if next_byte == IAC:
                output.append(IAC)
                i += 2
                consumed = i
                continue

            # Three-byte commands: WILL / WONT / DO / DONT.
            if next_byte in (WILL, WONT, DO, DONT):
                if i + 2 >= length:
                    break  # Incomplete – wait for more data.
                option = data[i + 2]
                ec = self._negotiate(next_byte, option, responses)
                if ec is not None:
                    echo_changed = ec
                i += 3
                consumed = i
                continue

            # Subnegotiation.
            if next_byte == SB:
                end = data.find(bytes([IAC, SE]), i + 2)
                if end == -1:
                    break  # Incomplete subnegotiation – wait for more data.
                self._subnegotiate(data[i + 2 : end], responses, gmcp_messages)
                i = end + 2
                consumed = i
                continue

            # Any other IAC command (GA, EOR, NOP, etc.) – skip.
            i += 2
            consumed = i

        # Drop everything fully consumed; retain any partial trailing sequence.
        del self._inbuf[:consumed]

        return bytes(output), bytes(responses), echo_changed, gmcp_messages

    def _negotiate(self, command, option, responses):
        """Handle WILL/WONT/DO/DONT negotiation.

        Returns True/False if the server ECHO state changed, else None.
        """
        echo_changed = None
        if command == WILL:
            if option in (OPT_ECHO, OPT_SGA, OPT_GMCP):
                responses.extend([IAC, DO, option])
            else:
                responses.extend([IAC, DONT, option])
            if option == OPT_ECHO and not self._server_echo:
                self._server_echo = True
                echo_changed = True
        elif command == WONT:
            responses.extend([IAC, DONT, option])
            if option == OPT_ECHO and self._server_echo:
                self._server_echo = False
                echo_changed = False
        elif command == DO:
            if option == OPT_NAWS:
                responses.extend([IAC, WILL, OPT_NAWS])
                # Answer with the browser's actual terminal size (cached from
                # its NAWS frames, the first of which is sent the moment the
                # websocket opens). 80x24 only as a last-resort default.
                cols, rows = self._naws or (80, 24)
                responses.extend([
                    IAC, SB, OPT_NAWS,
                    (cols >> 8) & 0xFF, cols & 0xFF,
                    (rows >> 8) & 0xFF, rows & 0xFF,
                    IAC, SE,
                ])
            elif option == OPT_TTYPE:
                responses.extend([IAC, WILL, OPT_TTYPE])
            else:
                responses.extend([IAC, WONT, option])
        elif command == DONT:
            responses.extend([IAC, WONT, option])
        return echo_changed

    def _subnegotiate(self, payload, responses, gmcp_messages):
        """Handle telnet subnegotiation."""
        if not payload:
            return

        option = payload[0]

        if option == OPT_GMCP:
            # GMCP body is "Package.Message <json>"; hand it to the HUD.
            gmcp_messages.append(
                payload[1:].decode("utf-8", errors="replace")
            )
            return

        if option == OPT_TTYPE and len(payload) >= 2 and payload[1] == 1:
            # TTYPE SEND request – reply with terminal type.
            responses.extend([IAC, SB, OPT_TTYPE, 0])  # IS
            responses.extend(b"xterm-256color")
            responses.extend([IAC, SE])
