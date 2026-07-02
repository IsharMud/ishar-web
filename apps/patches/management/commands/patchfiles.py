from django.core.management.base import BaseCommand

from apps.patches.models import Patch


class Command(BaseCommand):
    """Audit patch PDF files on disk against database records."""

    help = (
        "List each patch and whether its PDF exists on disk. "
        "Use --hide to set is_visible=False on patches with missing files."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--hide",
            action="store_true",
            help="Hide (is_visible=False) visible patches whose file is missing.",
        )

    def handle(self, *args, **options):
        missing = []

        for patch in Patch.objects.all():
            if patch.file_size is not None:
                self.stdout.write(
                    self.style.SUCCESS(f"OK      {patch.patch_file.name} ({patch})")
                )
            else:
                missing.append(patch)
                self.stdout.write(
                    self.style.ERROR(
                        f"MISSING {patch.patch_file.name} ({patch})"
                        f"{' [visible]' if patch.is_visible else ''}"
                    )
                )

        if not missing:
            self.stdout.write(self.style.SUCCESS("All patch files present."))
            return

        if options["hide"]:
            hidden = Patch.objects.filter(
                pk__in=[patch.pk for patch in missing], is_visible=True
            ).update(is_visible=False)
            self.stdout.write(
                self.style.WARNING(f"Hid {hidden} patch(es) with missing files.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"{len(missing)} patch file(s) missing. "
                    "Re-run with --hide to unpublish them."
                )
            )
