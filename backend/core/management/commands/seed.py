import os
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Carga todos los seeders (fixtures) de la carpeta seeders'

    def handle(self, *args, **options):
        seeders_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'seeders')
        
        # Lista de archivos seeders en orden de dependencias (primero los independientes)
        seeders = [
            'app.json',
            'categorias.json',
            'tipos_promocion.json',
            'supermercados.json',
            'usuarios.json',
            'promociones.json',
            'promociones_horarios.json',
            'valoraciones.json',
            'comentarios.json',
            'favoritos.json',
            'notificaciones.json',
            'usuario_notificaciones.json',
            'reportes.json',
        ]

        self.stdout.write(self.style.MIGRATE_HEADING('Cargando seeders...'))
        
        for seeder in seeders:
            filepath = os.path.join(seeders_dir, seeder)
            if os.path.exists(filepath):
                try:
                    call_command('loaddata', filepath, verbosity=0)
                    self.stdout.write(f'  ✓ {seeder}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  ✗ {seeder}: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠ {seeder}: archivo no encontrado'))

        self.stdout.write(self.style.SUCCESS('Seeders completados'))
