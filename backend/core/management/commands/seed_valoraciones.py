from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from promocion.models import Promocion
from usuario.models import Usuario
from valoracion.models import Valoracion
from .seed_utils import load_seed_data, reset_pk_sequence


class Command(BaseCommand):
    help = "Seed valoraciones from seeders/valoraciones.json."

    def handle(self, *args, **options):
        data = load_seed_data("valoraciones.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                valoracion_id = item["id"]
                usuario_id = item.get("id_usuario")
                codigo = item.get("codigo_promocion")

                if not usuario_id:
                    raise CommandError(f"Valoracion {valoracion_id}: id_usuario es obligatorio.")
                if not codigo:
                    raise CommandError(f"Valoracion {valoracion_id}: codigo_promocion es obligatorio.")

                usuario = Usuario.objects.get(id=usuario_id)
                promocion = Promocion.objects.get(codigo=codigo)

                defaults = {
                    "tipo": item.get("tipo"),
                    "id_usuario": usuario,
                    "codigo_promocion": promocion,
                }

                _, was_created = Valoracion.objects.update_or_create(
                    id=valoracion_id,
                    defaults=defaults,
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(Valoracion)
        self.stdout.write(self.style.SUCCESS(
            f"Valoraciones seeded. Created: {created}, Updated: {updated}."
        ))
