"""Signup forms. Field rules mirror the game's account creation
(``apps/accounts/validators.py``); uniqueness is checked here so a taken
e-mail or name reads as a field error, with the database's unique keys as
the race backstop."""
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from apps.accounts.models import Account
from apps.accounts.validators import (
    account_name_error, email_error, password_error,
)


class SignupEmailForm(forms.Form):
    email = forms.EmailField(
        max_length=29,
        label="E-mail Address",
        widget=forms.EmailInput(attrs={
            "autocomplete": "email",
            "autofocus": True,
            "class": "ac-input",
        }),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        error = email_error(email)
        if error:
            raise ValidationError(error)
        if Account.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "An account with that e-mail address already exists."
            )
        return email


class SignupVerifyForm(forms.Form):
    code = forms.RegexField(
        regex=r"^\d{6}$",
        label="Verification Code",
        error_messages={"invalid": "The code is the 6 digits from the e-mail."},
        widget=forms.TextInput(attrs={
            "autocomplete": "one-time-code",
            "inputmode": "numeric",
            "maxlength": "6",
            "class": "ac-input",
        }),
    )
    account_name = forms.CharField(
        min_length=3,
        max_length=13,
        label="Account Name",
        help_text="3-13 letters; this is what you'll log in with.",
        widget=forms.TextInput(attrs={
            "autocapitalize": "none",
            "autocomplete": "username",
            "class": "ac-input",
        }),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "ac-input",
        }),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "ac-input",
        }),
    )

    def __init__(self, *args, email="", **kwargs):
        super().__init__(*args, **kwargs)
        self.email = email

    def clean_account_name(self):
        name = self.cleaned_data["account_name"].strip().lower()
        error = account_name_error(name)
        if error:
            raise ValidationError(error)
        if Account.objects.filter(account_name__iexact=name).exists():
            raise ValidationError(
                "An account with that name already exists."
            )
        return name

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "The passwords don't match.")
        elif password1:
            error = password_error(
                password1,
                account_name=cleaned.get("account_name", ""),
                email=self.email,
            )
            if error:
                self.add_error("password1", error)
            else:
                try:
                    validate_password(password1)
                except ValidationError as exc:
                    self.add_error("password1", exc)
        return cleaned
