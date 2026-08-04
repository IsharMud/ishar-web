import sys

from django.db import migrations
from django.db.models import Q


# Verified dead as of August 2026 — gone from their store, or unable to run on
# any OS a player would connect from today:
#   MUDRammer  — pulled from the App Store by its developer, March 2025
#   Mukluk     — unpublished from Google Play, December 2024; broken on modern Android
#   BlowTorch  — abandoned since 2015; delisted, and its target SDK is too old
#                for Android 14+ to install
#   MudWalker  — 32-bit; cannot launch on macOS 10.15+ (2019)
#   zMUD       — unmaintained since ~2009; its successor CMUD is dead too
#   yTin       — dead since ~2003
#   Gosclient  — GNOME 1-era; project and site long gone
DEAD_CLIENTS = (
    "MUDRammer",
    "Mukluk",
    "BlowTorch",
    "MudWalker",
    "zMUD",
    "yTin",
    "Gosclient",
)

SAVITAR_NAME = "Savitar"
SAVITAR_URL = "https://www.heynow.com/savitar/"


def _macos_category(MUDClient, MUDClientCategory):
    # Anchor on a known macOS client so this works whatever the category is
    # named in the live table; hidden clients still anchor fine.
    for name in ("Atlantis", "MudWalker"):
        client = MUDClient.objects.filter(name__iexact=name).first()
        if client:
            return client.category
    return MUDClientCategory.objects.filter(name__icontains="mac").first()


def refresh_client_list(apps, schema_editor):
    MUDClient = apps.get_model("clients", "MUDClient")
    MUDClientCategory = apps.get_model("clients", "MUDClientCategory")

    dead = Q()
    for name in DEAD_CLIENTS:
        dead |= Q(name__iexact=name)
    MUDClient.objects.filter(dead).update(is_visible=False)

    category = _macos_category(MUDClient, MUDClientCategory)
    if category is None:
        print(
            "WARN: no macOS client category found — add Savitar "
            f"({SAVITAR_URL}) by hand in the admin.",
            file=sys.stderr,
        )
        return
    MUDClient.objects.get_or_create(
        name=SAVITAR_NAME,
        defaults={"category": category, "url": SAVITAR_URL},
    )


def restore_client_list(apps, schema_editor):
    MUDClient = apps.get_model("clients", "MUDClient")

    MUDClient.objects.filter(name__iexact=SAVITAR_NAME).delete()

    dead = Q()
    for name in DEAD_CLIENTS:
        dead |= Q(name__iexact=name)
    MUDClient.objects.filter(dead).update(is_visible=True)


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0008_mudclient_featured"),
    ]

    operations = [
        migrations.RunPython(refresh_client_list, restore_client_list),
    ]
