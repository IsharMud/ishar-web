"""Web signup: verify the e-mail first, then create the account.

Two steps. Step 1 takes an e-mail and sends a 6-digit code; step 2 takes
the code plus account name and password, creates the ``accounts`` row
already verified, and signs the player in. No account exists until the
code is confirmed, so the game's table never holds unverified signups.

Creation mirrors the game's gates: the season ``game_state`` closes
signup exactly when the telnet prompt refuses ``new`` (maintenance,
closed beta, season cycle). ``GLOBAL_DENY_ACCESS`` is in-game memory the
web can't see — a signup during that window succeeds but can't log in
until it lifts.
"""
import logging
import secrets
from datetime import timedelta
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import login
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import DatabaseError, IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.timezone import now
from django.views.generic.edit import FormView

from apps.core.forms import SignupEmailForm, SignupVerifyForm
from apps.core.models import SignupVerification
from apps.core.utils.ip import client_ip
from apps.seasons.models.season import GameState, Season
from apps.seasons.utils.current import get_current_season

from .mixins import NeverCacheMixin


logger = logging.getLogger(__name__)

SESSION_EMAIL_KEY = "signup_email"
SESSION_NEXT_KEY = "signup_next"
IP_SEND_LIMIT = 10          # sends per address per hour
IP_SEND_WINDOW = 60 * 60


def signup_gate_message():
    """None when account creation is open; otherwise the refusal copy.

    The refusal strings are the game's own (server.c, the ``new`` handler
    at the account prompt). Unknown state fails closed, matching the
    test-server policy's stance.
    """
    try:
        state = get_current_season().game_state
    except (Season.DoesNotExist, DatabaseError):
        return (
            "Account creation is temporarily unavailable — please try "
            "again in a few minutes."
        )
    if state == GameState.MAINTENANCE:
        return "Account creation is disabled for scheduled downtime."
    if state == GameState.CLOSED_BETA:
        return "Account creation is disabled during closed beta."
    if state == GameState.SEASON_CYCLE:
        return (
            "Account creation is disabled as Varenya weaves a new season."
        )
    return None


def _ip_send_allowed(request) -> bool:
    key = f"signup.send.{client_ip(request) or 'unknown'}"
    if cache.add(key, 1, IP_SEND_WINDOW):
        return True
    try:
        return cache.incr(key) <= IP_SEND_LIMIT
    except ValueError:
        cache.add(key, 1, IP_SEND_WINDOW)
        return True


def _send_code(request, email):
    """E-mail a fresh code and upsert the verification row.

    Returns an error string, or None on success. The mail is sent before
    the row is written so an SMTP failure leaves no phantom pending state.
    """
    if not _ip_send_allowed(request):
        return (
            "Too many verification e-mails from your address — try again "
            "in an hour."
        )

    current = SignupVerification.objects.filter(email__iexact=email).first()
    when = now()
    if current and current.expires_at > when:
        cooldown = timedelta(
            seconds=SignupVerification.RESEND_COOLDOWN_SECONDS
        )
        if when - current.last_sent_at < cooldown:
            return (
                "A code was just sent — give it a minute to arrive before "
                "asking for another."
            )
        if current.send_count >= SignupVerification.MAX_SENDS:
            return (
                "Too many codes sent to that address. Wait for the last "
                "one to expire, then start over."
            )

    code = f"{secrets.randbelow(10**6):06d}"
    try:
        send_mail(
            subject="Your verification code",
            message=(
                f"Your {settings.WEBSITE_TITLE} verification code is: "
                f"{code}\n\n"
                "It expires in 15 minutes. If you didn't request this, "
                "you can ignore this e-mail.\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except (SMTPException, OSError) as exc:
        logger.warning("Signup verification mail to %s failed: %s", email, exc)
        return (
            "We couldn't send the verification e-mail right now — please "
            "try again in a few minutes."
        )

    # An expired row restarts its counters; a live one keeps counting.
    resend = bool(current and current.expires_at > when)
    SignupVerification.objects.update_or_create(
        email=email,
        defaults={
            "code_hash": SignupVerification.hash_code(email, code),
            "expires_at": when + timedelta(
                seconds=SignupVerification.CODE_TTL_SECONDS
            ),
            "attempts": 0,
            "send_count": current.send_count + 1 if resend else 1,
            "last_sent_at": when,
        },
    )
    return None


def _stash_next(request):
    candidate = request.GET.get("next") or request.POST.get("next") or ""
    if candidate and url_has_allowed_host_and_scheme(
        candidate, allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        request.session[SESSION_NEXT_KEY] = candidate


class SignupView(NeverCacheMixin, FormView):
    """Step 1: take an e-mail address, send it a verification code."""

    template_name = "signup.html"
    form_class = SignupEmailForm
    success_url = reverse_lazy("signup_verify")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["step"] = "email"
        ctx["gate_message"] = signup_gate_message()
        return ctx

    def get(self, request, *args, **kwargs):
        _stash_next(request)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        _stash_next(self.request)
        gate = signup_gate_message()
        if gate:
            form.add_error(None, gate)
            return self.form_invalid(form)
        email = form.cleaned_data["email"]
        error = _send_code(self.request, email)
        if error:
            form.add_error(None, error)
            return self.form_invalid(form)
        self.request.session[SESSION_EMAIL_KEY] = email
        return super().form_valid(form)


class SignupVerifyView(NeverCacheMixin, FormView):
    """Step 2: code + account name + password creates the account."""

    template_name = "signup.html"
    form_class = SignupVerifyForm

    def dispatch(self, request, *args, **kwargs):
        self.email = request.session.get(SESSION_EMAIL_KEY, "")
        if not self.email:
            return HttpResponseRedirect(reverse("signup"))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["email"] = self.email
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["step"] = "verify"
        ctx["signup_email"] = self.email
        return ctx

    def post(self, request, *args, **kwargs):
        if request.POST.get("action") == "resend":
            error = _send_code(request, self.email)
            ctx = self.get_context_data(
                form=self.form_class(email=self.email)
            )
            if error:
                ctx["resend_error"] = error
            else:
                ctx["resend_notice"] = "A new code is on its way to your inbox."
            return self.render_to_response(ctx)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        gate = signup_gate_message()
        if gate:
            # A season cycle can start mid-flow; the code stays valid, so
            # the player can finish once the gate lifts.
            form.add_error(None, gate)
            return self.form_invalid(form)

        pending = SignupVerification.objects.filter(
            email__iexact=self.email
        ).first()
        if pending is None or pending.expires_at <= now():
            form.add_error(
                "code", "That code has expired — send yourself a new one."
            )
            return self.form_invalid(form)
        if not pending.matches(form.cleaned_data["code"]):
            pending.attempts += 1
            if pending.attempts >= SignupVerification.MAX_ATTEMPTS:
                pending.delete()
                form.add_error(
                    "code",
                    "Too many wrong codes — send yourself a new one.",
                )
            else:
                pending.save(update_fields=["attempts"])
                form.add_error("code", "That code isn't right.")
            return self.form_invalid(form)

        from apps.accounts.models import Account

        try:
            account = Account.objects.create_user(
                email=self.email,
                account_name=form.cleaned_data["account_name"],
                password=form.cleaned_data["password1"],
                ip=client_ip(self.request),
            )
        except IntegrityError:
            # Lost a race on email/name despite the form checks; the
            # unique keys are the authority (never upsert — ishar-mud#1711).
            form.add_error(
                None,
                "That e-mail address or account name was just taken — "
                "please adjust and try again.",
            )
            return self.form_invalid(form)

        pending.delete()
        del self.request.session[SESSION_EMAIL_KEY]
        login(self.request, account)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.session.pop(SESSION_NEXT_KEY, None) or "/connect/"
