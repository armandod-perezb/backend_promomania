from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from favorito.models import Favorito
from promocion.models import Promocion
from usuario.models import Usuario
from .seed_utils import (
    load_seed_data,
    parse_datetime,
    reset_pk_sequence,
    update_timestamp,
)


class Command(BaseCommand):
    help = "Seed favoritos from seeders/favoritos.json."

    def handle(self, *args, **options):
        data = load_seed_data("favoritos.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                favorito_id = item["id"]
                usuario_id = item.get("id_usuario")
                codigo = item.get("codigo_promocion")

                if not usuario_id:
                    raise CommandError(f"Favorito {favorito_id}: id_usuario es obligatorio.")
                if not codigo:
                    raise CommandError(f"Favorito {favorito_id}: codigo_promocion es obligatorio.")

                usuario = Usuario.objects.get(id=usuario_id)
                promocion = Promocion.objects.get(codigo=codigo)

                defaults = {
                    "id_usuario": usuario,
                    "codigo_promocion": promocion,
                }

                _, was_created = Favorito.objects.update_or_create(
                    id=favorito_id,
                    defaults=defaults,
                )
                update_timestamp(
                    Favorito,
                    favorito_id,
                    "fecha",
                    parse_datetime(item.get("fecha")),
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(Favorito)
        self.stdout.write(self.style.SUCCESS(
            f"Favoritos seeded. Created: {created}, Updated: {updated}."
        ))
