from django.core.management.base import BaseCommand
from django.db import transaction

from notificacion.models import Notificacion
from .seed_utils import (
    load_seed_data,
    parse_datetime,
    reset_pk_sequence,
    update_timestamp,
)


class Command(BaseCommand):
    help = "Seed notificaciones from seeders/notificaciones.json."

    @staticmethod
    def _map_legacy_tipo(raw_tipo: str | None) -> str:
        if not raw_tipo:
            return "general"
        mapping = {
            "action_executer": "accion_ejecutor",
            "action_receiver": "accion_receptor",
            "action_controller": "accion_controlador",
        }
        return mapping.get(raw_tipo, raw_tipo)

    def handle(self, *args, **options):
        data = load_seed_data("notificaciones.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                notificacion_id = item["id"]
                defaults = {
                    "mensaje": item.get("mensaje", "").strip(),
                    "tipo": self._map_legacy_tipo(item.get("tipo") or item.get("t_notificacion")),
                    "id_usuario_destino_id": item.get("id_usuario_destino"),
                    "leida": item.get("leida", False),
                }
                _, was_created = Notificacion.objects.update_or_create(
                    id=notificacion_id,
                    defaults=defaults,
                )
                update_timestamp(
                    Notificacion,
                    notificacion_id,
                    "fecha",
                    parse_datetime(item.get("fecha")),
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(Notificacion)
        self.stdout.write(self.style.SUCCESS(
            f"Notificaciones seeded. Created: {created}, Updated: {updated}."
        ))
