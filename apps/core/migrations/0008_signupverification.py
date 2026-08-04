import apps.core.models.unsigned
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_webadmintask"),
    ]

    operations = [
        migrations.CreateModel(
            name="SignupVerification",
            fields=[
                (
                    "id",
                    apps.core.models.unsigned.UnsignedAutoField(
                        primary_key=True, serialize=False
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="E-mail address being verified.",
                        max_length=30,
                        unique=True,
                        verbose_name="E-mail Address",
                    ),
                ),
                (
                    "code_hash",
                    models.CharField(
                        help_text=(
                            "SHA-256 of 'email:code'; the code itself is "
                            "never stored."
                        ),
                        max_length=64,
                        verbose_name="Code Hash",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created At"
                    ),
                ),
                (
                    "expires_at",
                    models.DateTimeField(
                        help_text=(
                            "Codes are valid for 15 minutes from the last "
                            "send."
                        ),
                        verbose_name="Expires At",
                    ),
                ),
                (
                    "attempts",
                    models.PositiveSmallIntegerField(
                        default=0,
                        help_text=(
                            "Wrong-code attempts; the row is deleted at "
                            "the cap."
                        ),
                        verbose_name="Attempts",
                    ),
                ),
                (
                    "send_count",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="Send Count"
                    ),
                ),
                (
                    "last_sent_at",
                    models.DateTimeField(verbose_name="Last Sent At"),
                ),
            ],
            options={
                "verbose_name": "Signup Verification",
                "verbose_name_plural": "Signup Verifications",
                "db_table": "web_signup_verification",
                "managed": True,
            },
        ),
    ]
