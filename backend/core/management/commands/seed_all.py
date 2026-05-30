from django.core.management import call_command
from django.core.management.base import BaseCommand

from categoria.models import Categoria
from comentario.models import Comentario
from favorito.models import Favorito
from notificacion.models import Notificacion
from promocion.models import Promocion, PromocionHorario, TipoPromocion
from reporte.models import Reporte
from supermercado.models import Supermercado
from usuario.models import Usuario
from valoracion.models import Valoracion


class Command(BaseCommand):
    help = "Run all seed commands in the correct order."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            default=False,
            help="Seed even if data already exists.",
        )

    def handle(self, *args, **options):
        force = options.get("force", False)
        if not force:
            if self._has_data():
                self.stdout.write(self.style.WARNING(
                    "Seed data already exists. Skipping all seeders."
                ))
                return

        call_command("seed_app")
        call_command("seed_usuarios")
        call_command("seed_supermercados")
        call_command("seed_categorias")
        call_command("seed_tipos_promocion")
        call_command("seed_promociones")
        call_command("seed_promociones_horarios")
        call_command("seed_notificaciones")
        call_command("seed_comentarios")
        call_command("seed_favoritos")
        call_command("seed_valoraciones")
        call_command("seed_reportes")

        self.stdout.write(self.style.SUCCESS("All seeders completed."))

    def _has_data(self):
        return any([
            Usuario.objects.exists(),
            Supermercado.objects.exists(),
            Categoria.objects.exists(),
            TipoPromocion.objects.exists(),
            Promocion.objects.exists(),
            PromocionHorario.objects.exists(),
            Notificacion.objects.exists(),
            Comentario.objects.exists(),
            Favorito.objects.exists(),
            Valoracion.objects.exists(),
            Reporte.objects.exists(),
        ])
