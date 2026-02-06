"""WebSocket consumer that proxies to a telnet MUD server."""
import asyncio
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings


logger = logging.getLogger(__name__)

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
            await self.close()
            return

        await self.accept()

        # Read from the MUD in the background.
        self._read_task = asyncio.create_task(self._read_telnet())

    async def disconnect(self, code):
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
        if not self._writer or self._writer.is_closing():
            return

        if text_data:
            self._writer.write(text_data.encode("utf-8", errors="replace"))
            try:
                await self._writer.drain()
            except (ConnectionError, OSError):
                await self.close()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _read_telnet(self):
        """Continuously read from the MUD and forward to the WebSocket."""
        try:
            while True:
                data = await self._reader.read(4096)
                if not data:
                    await self.close()
                    return

                display_data, responses = self._process_telnet(data)

                # Send any telnet negotiation replies.
                if responses and self._writer and not self._writer.is_closing():
                    self._writer.write(responses)
                    try:
                        await self._writer.drain()
                    except (ConnectionError, OSError):
                        await self.close()
                        return

                # Forward displayable text to the browser.
                if display_data:
                    await self.send(
                        text_data=display_data.decode(
                            "utf-8", errors="replace"
                        )
                    )
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            logger.error("Telnet read error: %s", exc)
            await self.close()

    def _process_telnet(self, data):
        """Strip telnet IAC sequences, returning (display_bytes, response_bytes)."""
        output = bytearray()
        responses = bytearray()
        i = 0
        length = len(data)

        while i < length:
            byte = data[i]

            if byte != IAC:
                output.append(byte)
                i += 1
                continue

            # IAC at end of buffer – treat as literal.
            if i + 1 >= length:
                output.append(byte)
                i += 1
                continue

            next_byte = data[i + 1]

            # Escaped 0xFF.
            if next_byte == IAC:
                output.append(IAC)
                i += 2
                continue

            # Three-byte commands: WILL / WONT / DO / DONT.
            if next_byte in (WILL, WONT, DO, DONT):
                if i + 2 >= length:
                    break  # Incomplete – wait for more data.
                option = data[i + 2]
                self._negotiate(next_byte, option, responses)
                i += 3
                continue

            # Subnegotiation.
            if next_byte == SB:
                end = data.find(bytes([IAC, SE]), i + 2)
                if end == -1:
                    break  # Incomplete subnegotiation.
                self._subnegotiate(data[i + 2 : end], responses)
                i = end + 2
                continue

            # Any other IAC command (GA, NOP, etc.) – skip.
            i += 2

        return bytes(output), bytes(responses)

    def _negotiate(self, command, option, responses):
        """Handle WILL/WONT/DO/DONT negotiation."""
        if command == WILL:
            if option in (OPT_ECHO, OPT_SGA):
                responses.extend([IAC, DO, option])
            else:
                responses.extend([IAC, DONT, option])
        elif command == DO:
            if option == OPT_NAWS:
                responses.extend([IAC, WILL, OPT_NAWS])
                # Send default window size 80x24.
                responses.extend([
                    IAC, SB, OPT_NAWS,
                    0, 80,
                    0, 24,
                    IAC, SE,
                ])
            elif option == OPT_TTYPE:
                responses.extend([IAC, WILL, OPT_TTYPE])
            else:
                responses.extend([IAC, WONT, option])
        elif command == DONT:
            responses.extend([IAC, WONT, option])
        elif command == WONT:
            responses.extend([IAC, DONT, option])

    def _subnegotiate(self, payload, responses):
        """Handle telnet subnegotiation."""
        if not payload:
            return

        option = payload[0]

        if option == OPT_TTYPE and len(payload) >= 2 and payload[1] == 1:
            # TTYPE SEND request – reply with terminal type.
            responses.extend([IAC, SB, OPT_TTYPE, 0])  # IS
            responses.extend(b"xterm-256color")
            responses.extend([IAC, SE])
