from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from categoria.models import Categoria
from promocion.models import Promocion, TipoPromocion
from supermercado.models import Supermercado
from usuario.models import Usuario
from .seed_utils import load_seed_data, parse_date


class Command(BaseCommand):
    help = "Seed promociones from seeders/promociones.json."

    def handle(self, *args, **options):
        data = load_seed_data("promociones.json")
        created = 0
        updated = 0
        with transaction.atomic():
            for item in data:
                codigo = item["codigo"]
                usuario_id = item.get("id_usuario")
                supermercado_id = item.get("id_supermercado")
                categoria_id = item.get("id_categoria")
                tipo_id = item.get("id_tipo_promocion")

                if not usuario_id:
                    raise CommandError(f"Promocion {codigo}: id_usuario es obligatorio.")
                if not supermercado_id:
                    raise CommandError(f"Promocion {codigo}: id_supermercado es obligatorio.")
                if not categoria_id:
                    raise CommandError(f"Promocion {codigo}: id_categoria es obligatorio.")
                if not tipo_id:
                    raise CommandError(f"Promocion {codigo}: id_tipo_promocion es obligatorio.")

                try:
                    usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None
                except Usuario.DoesNotExist as exc:
                    raise CommandError(f"Usuario not found: {usuario_id}") from exc

                try:
                    supermercado = (
                        Supermercado.objects.get(id=supermercado_id)
                        if supermercado_id else None
                    )
                except Supermercado.DoesNotExist as exc:
                    raise CommandError(f"Supermercado not found: {supermercado_id}") from exc

                try:
                    categoria = (
                        Categoria.objects.get(id=categoria_id)
                        if categoria_id else None
                    )
                except Categoria.DoesNotExist as exc:
                    raise CommandError(f"Categoria not found: {categoria_id}") from exc

                try:
                    tipo = (
                        TipoPromocion.objects.get(id=tipo_id)
                        if tipo_id else None
                    )
                except TipoPromocion.DoesNotExist as exc:
                    raise CommandError(f"TipoPromocion not found: {tipo_id}") from exc

                defaults = {
                    "titulo": item.get("titulo", "").strip(),
                    "descripcion": item.get("descripcion"),
                    "precio": item.get("precio", 0),
                    "descuento": item.get("descuento"),
                    "condicion_producto": item.get("condicion_producto", "nuevo"),
                    "ubicacion": item.get("ubicacion"),
                    "url": item.get("url"),
                    "foto": item.get("foto"),
                    "foto_es_local": item.get("foto_es_local", False),
                    "tipo_vigencia": item.get("tipo_vigencia", "por_fecha"),
                    "fecha_inicio": parse_date(item.get("fecha_inicio")),
                    "fecha_fin": parse_date(item.get("fecha_fin")),
                    "estado": item.get("estado", "pendiente"),
                    "vistas": item.get("vistas", 0),
                    "lat": item.get("lat"),
                    "lng": item.get("lng"),
                    "id_usuario": usuario,
                    "id_supermercado": supermercado,
                    "id_categoria": categoria,
                    "id_tipo_promocion": tipo,
                }

                _, was_created = Promocion.objects.update_or_create(
                    codigo=codigo,
                    defaults=defaults,
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        self.stdout.write(self.style.SUCCESS(
            f"Promociones seeded. Created: {created}, Updated: {updated}."
        ))
