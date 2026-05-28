from django.core.management.base import BaseCommand
from django.db import transaction

from supermercado.models import Supermercado
from .seed_utils import load_seed_data, reset_pk_sequence


class Command(BaseCommand):
    help = "Seed supermercados from seeders/supermercados.json."

    def handle(self, *args, **options):
        data = load_seed_data("supermercados.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                sup_id = item["id"]
                defaults = {
                    "nombre": item.get("nombre", "").strip(),
                    "direccion": item.get("direccion"),
                    "ciudad": item.get("ciudad"),
                    "estado": item.get("estado", "activo"),
                }
                _, was_created = Supermercado.objects.update_or_create(
                    id=sup_id,
                    defaults=defaults,
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(Supermercado)
        self.stdout.write(self.style.SUCCESS(
            f"Supermercados seeded. Created: {created}, Updated: {updated}."
        ))
