from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from comentario.models import Comentario
from promocion.models import Promocion
from usuario.models import Usuario
from .seed_utils import (
    load_seed_data,
    parse_datetime,
    reset_pk_sequence,
    update_timestamp,
)


class Command(BaseCommand):
    help = "Seed comentarios from seeders/comentarios.json."

    def handle(self, *args, **options):
        data = load_seed_data("comentarios.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                comment_id = item["id"]
                usuario_id = item.get("id_usuario")
                codigo = item.get("codigo_promocion")
                reply_id = item.get("id_comment_reply")

                if not usuario_id:
                    raise CommandError(f"Comentario {comment_id}: id_usuario es obligatorio.")
                if not codigo:
                    raise CommandError(f"Comentario {comment_id}: codigo_promocion es obligatorio.")

                usuario = Usuario.objects.get(id=usuario_id)
                promocion = Promocion.objects.get(codigo=codigo)
                reply = Comentario.objects.get(id=reply_id) if reply_id else None

                defaults = {
                    "contenido": item.get("contenido", "").strip(),
                    "id_usuario": usuario,
                    "codigo_promocion": promocion,
                    "id_comment_reply": reply,
                }

                _, was_created = Comentario.objects.update_or_create(
                    id=comment_id,
                    defaults=defaults,
                )
                update_timestamp(
                    Comentario,
                    comment_id,
                    "fecha",
                    parse_datetime(item.get("fecha")),
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(Comentario)
        self.stdout.write(self.style.SUCCESS(
            f"Comentarios seeded. Created: {created}, Updated: {updated}."
        ))
