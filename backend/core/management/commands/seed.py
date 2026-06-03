import os
import json
from datetime import datetime, time
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Carga todos los seeders de la carpeta seeders'

    def load_json(self, filename):
        """Carga un archivo JSON de la carpeta seeders"""
        seeders_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'seeders'
        )
        filepath = os.path.join(seeders_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def seed_categorias(self):
        from categoria.models import Categoria
        data = self.load_json('categorias.json')
        if not data:
            return 0
        count = 0
        for item in data:
            _, created = Categoria.objects.get_or_create(
                id=item['id'],
                defaults={'nombre': item['nombre'], 'descripcion': item.get('descripcion')}
            )
            if created:
                count += 1
        return count

    def seed_tipos_promocion(self):
        from promocion.models import TipoPromocion
        data = self.load_json('tipos_promocion.json')
        if not data:
            return 0
        count = 0
        for item in data:
            _, created = TipoPromocion.objects.get_or_create(
                id=item['id'],
                defaults={
                    'nombre': item['nombre'],
                    'descripcion': item.get('descripcion'),
                    'estado': item.get('estado', 'activo')
                }
            )
            if created:
                count += 1
        return count

    def seed_supermercados(self):
        from supermercado.models import Supermercado
        data = self.load_json('supermercados.json')
        if not data:
            return 0
        count = 0
        for item in data:
            _, created = Supermercado.objects.get_or_create(
                id=item['id'],
                defaults={
                    'nombre': item['nombre'],
                    'direccion': item.get('direccion'),
                    'ciudad': item.get('ciudad'),
                    'estado': item.get('estado', 'activo')
                }
            )
            if created:
                count += 1
        return count

    def seed_usuarios(self):
        from usuario.models import Usuario
        data = self.load_json('usuarios.json')
        if not data:
            return 0
        count = 0
        for item in data:
            _, created = Usuario.objects.get_or_create(
                id=item['id'],
                defaults={
                    'nombre': item['nombre'],
                    'correo': item['correo'],
                    'password': item['password'],
                    'ciudad': item.get('ciudad'),
                    'nivel': item.get('nivel'),
                    'puntuacion': item.get('puntuacion'),
                    'rol': item.get('rol', 'usuario'),
                    'estado': item.get('estado', 'activo')
                }
            )
            if created:
                count += 1
        return count

    def seed_promociones(self):
        from promocion.models import Promocion
        from usuario.models import Usuario
        from supermercado.models import Supermercado
        from categoria.models import Categoria
        from promocion.models import TipoPromocion
        data = self.load_json('promociones.json')
        if not data:
            return 0
        count = 0
        for item in data:
            try:
                usuario = Usuario.objects.get(id=item['id_usuario'])
                supermercado = Supermercado.objects.get(id=item['id_supermercado'])
                categoria = Categoria.objects.get(id=item['id_categoria'])
                tipo_promocion = TipoPromocion.objects.get(id=item['id_tipo_promocion'])

                fecha_inicio = item.get('fecha_inicio')
                fecha_fin = item.get('fecha_fin')
                if fecha_inicio:
                    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                if fecha_fin:
                    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

                _, created = Promocion.objects.get_or_create(
                    codigo=item['codigo'],
                    defaults={
                        'titulo': item['titulo'],
                        'descripcion': item.get('descripcion'),
                        'precio': item['precio'],
                        'descuento': item.get('descuento'),
                        'condicion_producto': item.get('condicion_producto', 'nuevo'),
                        'ubicacion': item.get('ubicacion'),
                        'url': item.get('url'),
                        'foto': item.get('foto'),
                        'foto_es_local': item.get('foto_es_local', False),
                        'tipo_vigencia': item.get('tipo_vigencia', 'por_fecha'),
                        'fecha_inicio': fecha_inicio,
                        'fecha_fin': fecha_fin,
                        'estado': item.get('estado', 'pendiente'),
                        'vistas': item.get('vistas', 0),
                        'lat': item.get('lat'),
                        'lng': item.get('lng'),
                        'id_usuario': usuario,
                        'id_supermercado': supermercado,
                        'id_categoria': categoria,
                        'id_tipo_promocion': tipo_promocion,
                    }
                )
                if created:
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"    Error en promoción {item.get('codigo')}: {e}"))
        return count

    def seed_promociones_horarios(self):
        from promocion.models import PromocionHorario, Promocion
        data = self.load_json('promociones_horarios.json')
        if not data:
            return 0
        count = 0
        for item in data:
            try:
                promocion = Promocion.objects.get(codigo=item['codigo_promocion'])

                def parse_time(t):
                    if isinstance(t, str):
                        # Soporta formato HH:MM o HH:MM:SS
                        parts = t.split(':')
                        hour = int(parts[0])
                        minute = int(parts[1])
                        second = int(parts[2]) if len(parts) > 2 else 0
                        return time(hour, minute, second)
                    elif isinstance(t, dict):
                        return time(t['hour'], t['minute'], t.get('second', 0))
                    return t

                hora_inicio = parse_time(item['hora_inicio'])
                hora_fin = parse_time(item['hora_fin'])

                _, created = PromocionHorario.objects.get_or_create(
                    id=item['id'],
                    defaults={
                        'dia_semana': item['dia_semana'],
                        'hora_inicio': hora_inicio,
                        'hora_fin': hora_fin,
                        'codigo_promocion': promocion
                    }
                )
                if created:
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"    Error en horario {item.get('id')}: {e}"))
        return count

    def seed_valoraciones(self):
        from valoracion.models import Valoracion
        from usuario.models import Usuario
        from promocion.models import Promocion
        data = self.load_json('valoraciones.json')
        if not data:
            return 0
        count = 0
        for item in data:
            try:
                usuario = Usuario.objects.get(id=item['id_usuario'])
                promocion = Promocion.objects.get(codigo=item['codigo_promocion'])
                _, created = Valoracion.objects.get_or_create(
                    id=item['id'],
                    defaults={
                        'tipo': item['tipo'],
                        'id_usuario': usuario,
                        'codigo_promocion': promocion
                    }
                )
                if created:
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"    Error en valoración {item.get('id')}: {e}"))
        return count

    def seed_comentarios(self):
        from comentario.models import Comentario
        from usuario.models import Usuario
        from promocion.models import Promocion
        from datetime import datetime
        data = self.load_json('comentarios.json')
        if not data:
            return 0
        count = 0
        for item in data:
            try:
                usuario = Usuario.objects.get(id=item['id_usuario'])
                promocion = Promocion.objects.get(codigo=item['codigo_promocion'])
                
                fecha = item.get('fecha')
                if fecha:
                    fecha = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
                
                id_comment_reply = item.get('id_comment_reply')
                reply_obj = None
                if id_comment_reply:
                    reply_obj = Comentario.objects.filter(id=id_comment_reply).first()
                
                _, created = Comentario.objects.get_or_create(
                    id=item['id'],
                    defaults={
                        'contenido': item['contenido'],
                        'fecha': fecha,
                        'id_usuario': usuario,
                        'codigo_promocion': promocion,
                        'id_comment_reply': reply_obj
                    }
                )
                if created:
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"    Error en comentario {item.get('id')}: {e}"))
        return count

    def seed_favoritos(self):
        from favorito.models import Favorito
        from usuario.models import Usuario
        from promocion.models import Promocion
        from datetime import datetime
        data = self.load_json('favoritos.json')
        if not data:
            return 0
        count = 0
        for item in data:
            try:
                usuario = Usuario.objects.get(id=item['id_usuario'])
                promocion = Promocion.objects.get(codigo=item['codigo_promocion'])
                
                fecha = item.get('fecha')
                if fecha:
                    fecha = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
                
                _, created = Favorito.objects.get_or_create(
                    id=item['id'],
                    defaults={
                        'fecha': fecha,
                        'id_usuario': usuario,
                        'codigo_promocion': promocion
                    }
                )
                if created:
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"    Error en favorito {item.get('id')}: {e}"))
        return count

    def seed_notificaciones(self):
        from notificacion.models import Notificacion
        from usuario.models import Usuario
        from datetime import datetime
        data = self.load_json('notificaciones.json')
        if not data:
            return 0
        count = 0
        for item in data:
            try:
                fecha = item.get('fecha')
                if fecha:
                    fecha = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
                
                # El JSON usa 't_notificacion', el modelo usa 'tipo'
                tipo = item.get('t_notificacion', 'general')

                _, created = Notificacion.objects.get_or_create(
                    id=item['id'],
                    defaults={
                        'mensaje': item['mensaje'],
                        'fecha': fecha,
                        'tipo': tipo,
                        'leida': False
                    }
                )
                if created:
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"    Error en notificación {item.get('id')}: {e}"))
        return count

    def seed_usuario_notificaciones(self):
        # Este modelo no existe en la versión actual - se omite
        return 0

    def seed_reportes(self):
        from reporte.models import Reporte
        from usuario.models import Usuario
        from promocion.models import Promocion
        from datetime import datetime
        data = self.load_json('reportes.json')
        if not data:
            return 0
        count = 0
        for item in data:
            try:
                usuario = Usuario.objects.get(id=item['id_usuario'])
                promocion = Promocion.objects.get(codigo=item['codigo_promocion'])
                
                fecha = item.get('fecha')
                if fecha:
                    fecha = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
                
                _, created = Reporte.objects.get_or_create(
                    id=item['id'],
                    defaults={
                        'motivo': item['motivo'],
                        'estado': item.get('estado', 'pendiente'),
                        'fecha': fecha,
                        'id_usuario': usuario,
                        'codigo_promocion': promocion
                    }
                )
                if created:
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"    Error en reporte {item.get('id')}: {e}"))
        return count

    def handle(self, *args, **options):
        seeders_config = [
            ('Categorias', self.seed_categorias),
            ('Tipos de Promoción', self.seed_tipos_promocion),
            ('Supermercados', self.seed_supermercados),
            ('Usuarios', self.seed_usuarios),
            ('Promociones', self.seed_promociones),
            ('Horarios de Promociones', self.seed_promociones_horarios),
            ('Valoraciones', self.seed_valoraciones),
            ('Comentarios', self.seed_comentarios),
            ('Favoritos', self.seed_favoritos),
            ('Notificaciones', self.seed_notificaciones),
            ('Reportes', self.seed_reportes),
        ]

        self.stdout.write(self.style.MIGRATE_HEADING('Cargando seeders...'))

        with transaction.atomic():
            for name, seeder_func in seeders_config:
                try:
                    count = seeder_func()
                    self.stdout.write(f'  ✓ {name}: {count} creados')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  ✗ {name}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Seeders completados'))
