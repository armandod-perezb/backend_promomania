from django.core.management.base import BaseCommand

from .seed_utils import load_seed_data


class Command(BaseCommand):
    help = "Validates the app seed file."

    def handle(self, *args, **options):
        app_data = load_seed_data("app.json")
        name = app_data.get("name", "unknown")
        version = app_data.get("version", "unknown")
        self.stdout.write(self.style.SUCCESS(
            f"App seed loaded: {name} ({version})"
        ))
