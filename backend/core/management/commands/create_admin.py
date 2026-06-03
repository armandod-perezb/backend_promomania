from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Crea el usuario admin de Django si no existe'

    def handle(self, *args, **options):
        # Obtener credenciales de variables de entorno o usar valores por defecto
        username = os.getenv('DJANGO_ADMIN_USERNAME', 'admin')
        email = os.getenv('DJANGO_ADMIN_EMAIL', 'admin@promomania.com')
        password = os.getenv('DJANGO_ADMIN_PASSWORD', 'admin123')

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario "{username}" ya existe. Omitiendo...')
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(f'Usuario admin "{username}" creado exitosamente')
        )
