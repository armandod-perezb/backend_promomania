from django.core.management.base import BaseCommand
from django.db import transaction

from notificacion.models import Notificacion
from usuario.models import Usuario, UsuarioNotificacion
from .seed_utils import (
    load_seed_data,
    parse_datetime,
    reset_pk_sequence,
    update_timestamp,
)


class Command(BaseCommand):
    help = "Seed usuario notificaciones from seeders/usuario_notificaciones.json."

    def handle(self, *args, **options):
        data = load_seed_data("usuario_notificaciones.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                record_id = item["id"]
                usuario_id = item.get("id_usuario")
                notificacion_id = item.get("id_notificacion")

                usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None
                notificacion = (
                    Notificacion.objects.get(id=notificacion_id)
                    if notificacion_id else None
                )

                defaults = {
                    "id_usuario": usuario,
                    "id_notificacion": notificacion,
                    "leida": item.get("leida", False),
                }

                _, was_created = UsuarioNotificacion.objects.update_or_create(
                    id=record_id,
                    defaults=defaults,
                )
                update_timestamp(
                    UsuarioNotificacion,
                    record_id,
                    "fecha_recibida",
                    parse_datetime(item.get("fecha_recibida")),
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(UsuarioNotificacion)
        self.stdout.write(self.style.SUCCESS(
            f"UsuarioNotificacion seeded. Created: {created}, Updated: {updated}."
        ))
