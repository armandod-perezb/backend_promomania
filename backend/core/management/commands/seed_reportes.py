from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from promocion.models import Promocion
from reporte.models import Reporte
from usuario.models import Usuario
from .seed_utils import (
    load_seed_data,
    parse_datetime,
    reset_pk_sequence,
    update_timestamp,
)


class Command(BaseCommand):
    help = "Seed reportes from seeders/reportes.json."

    def handle(self, *args, **options):
        data = load_seed_data("reportes.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                reporte_id = item["id"]
                usuario_id = item.get("id_usuario")
                codigo = item.get("codigo_promocion")

                if not usuario_id:
                    raise CommandError(f"Reporte {reporte_id}: id_usuario es obligatorio.")
                if not codigo:
                    raise CommandError(f"Reporte {reporte_id}: codigo_promocion es obligatorio.")

                usuario = Usuario.objects.get(id=usuario_id)
                promocion = Promocion.objects.get(codigo=codigo)

                defaults = {
                    "motivo": item.get("motivo", "").strip(),
                    "estado": item.get("estado", "pendiente"),
                    "id_usuario": usuario,
                    "codigo_promocion": promocion,
                }

                _, was_created = Reporte.objects.update_or_create(
                    id=reporte_id,
                    defaults=defaults,
                )
                update_timestamp(
                    Reporte,
                    reporte_id,
                    "fecha",
                    parse_datetime(item.get("fecha")),
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(Reporte)
        self.stdout.write(self.style.SUCCESS(
            f"Reportes seeded. Created: {created}, Updated: {updated}."
        ))
