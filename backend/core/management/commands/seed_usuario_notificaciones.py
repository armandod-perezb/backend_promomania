from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Deprecated: usuario_notificaciones no longer exists in the current schema."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            "Skipping seed_usuario_notificaciones: table usuario_notificaciones was removed. "
            "Use seed_notificaciones with id_usuario_destino/leida instead."
        ))
