from django.core.management.base import BaseCommand
from django.db import transaction

from categoria.models import Categoria
from .seed_utils import load_seed_data, reset_pk_sequence


class Command(BaseCommand):
    help = "Seed categorias from seeders/categorias.json."

    def handle(self, *args, **options):
        data = load_seed_data("categorias.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                cat_id = item["id"]
                defaults = {
                    "nombre": item.get("nombre", "").strip(),
                    "descripcion": item.get("descripcion"),
                }
                _, was_created = Categoria.objects.update_or_create(
                    id=cat_id,
                    defaults=defaults,
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(Categoria)
        self.stdout.write(self.style.SUCCESS(
            f"Categorias seeded. Created: {created}, Updated: {updated}."
        ))
