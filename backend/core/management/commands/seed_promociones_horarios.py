from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from promocion.models import Promocion, PromocionHorario
from .seed_utils import load_seed_data, parse_time, reset_pk_sequence


class Command(BaseCommand):
    help = "Seed promociones horarios from seeders/promociones_horarios.json."

    def handle(self, *args, **options):
        data = load_seed_data("promociones_horarios.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                horario_id = item["id"]
                codigo = item.get("codigo_promocion")
                if not codigo:
                    raise CommandError(
                        f"PromocionHorario {horario_id}: codigo_promocion es obligatorio."
                    )
                promocion = Promocion.objects.get(codigo=codigo)

                defaults = {
                    "dia_semana": item.get("dia_semana"),
                    "hora_inicio": parse_time(item.get("hora_inicio")),
                    "hora_fin": parse_time(item.get("hora_fin")),
                    "codigo_promocion": promocion,
                }

                _, was_created = PromocionHorario.objects.update_or_create(
                    id=horario_id,
                    defaults=defaults,
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(PromocionHorario)
        self.stdout.write(self.style.SUCCESS(
            f"Promociones horarios seeded. Created: {created}, Updated: {updated}."
        ))
