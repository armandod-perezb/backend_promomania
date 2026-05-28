from django.core.management.base import BaseCommand
from django.db import transaction

from promocion.models import TipoPromocion
from .seed_utils import load_seed_data, reset_pk_sequence


class Command(BaseCommand):
    help = "Seed tipos de promocion from seeders/tipos_promocion.json."

    def handle(self, *args, **options):
        data = load_seed_data("tipos_promocion.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                tipo_id = item["id"]
                defaults = {
                    "nombre": item.get("nombre", "").strip(),
                    "descripcion": item.get("descripcion"),
                    "estado": item.get("estado", "activo"),
                }
                _, was_created = TipoPromocion.objects.update_or_create(
                    id=tipo_id,
                    defaults=defaults,
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(TipoPromocion)
        self.stdout.write(self.style.SUCCESS(
            f"Tipos de promocion seeded. Created: {created}, Updated: {updated}."
        ))
