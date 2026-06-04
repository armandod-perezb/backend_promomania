from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction

from usuario.models import Usuario
from .seed_utils import load_seed_data, reset_pk_sequence


class Command(BaseCommand):
    help = "Seed usuarios from seeders/usuarios.json."

    def handle(self, *args, **options):
        data = load_seed_data("usuarios.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                user_id = item["id"]
                defaults = {
                    "nombre": item.get("nombre", "").strip(),
                    "correo": item.get("correo", "").strip().lower(),
                    "password": make_password(item.get("password", "")),
                    "ciudad": item.get("ciudad"),
                    "nivel": item.get("nivel", 1),
                    "puntuacion": item.get("puntuacion", 0),
                    "rol": item.get("rol", "usuario"),
                    "estado": item.get("estado", "activo"),
                }
                _, was_created = Usuario.objects.update_or_create(
                    id=user_id,
                    defaults=defaults,
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        reset_pk_sequence(Usuario)
        self.stdout.write(self.style.SUCCESS(
            f"Usuarios seeded. Created: {created}, Updated: {updated}."
        ))
