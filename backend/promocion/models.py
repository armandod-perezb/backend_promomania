from django.db import models
from django.db.models import Q
from categoria.models import Categoria
from supermercado.models import Supermercado
from usuario.models import Usuario


class TipoPromocion(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tipos_promocion'


class Promocion(models.Model):
    CONDICION_PRODUCTO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
        ('reacondicionado', 'Reacondicionado'),
    ]

    TIPO_VIGENCIA_CHOICES = [
        ('por_fecha', 'Por Fecha'),
        ('permanente', 'Permanente'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    codigo = models.CharField(max_length=40, primary_key=True)
    titulo = models.CharField(max_length=180)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.IntegerField(null=True, blank=True)
    condicion_producto = models.CharField(
        max_length=30,
        choices=CONDICION_PRODUCTO_CHOICES,
        default='nuevo',
    )
    ubicacion = models.CharField(max_length=200, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    foto = models.TextField(null=True, blank=True)
    foto_es_local = models.BooleanField(default=False)
    tipo_vigencia = models.CharField(
        max_length=20,
        choices=TIPO_VIGENCIA_CHOICES,
        default='por_fecha',
    )
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    vistas = models.IntegerField(default=0)
    lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    lng = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='promociones',
    )
    id_supermercado = models.ForeignKey(
        Supermercado,
        on_delete=models.CASCADE,
        db_column='id_supermercado',
        related_name='promociones',
    )
    id_categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        db_column='id_categoria',
        related_name='promociones',
    )
    id_tipo_promocion = models.ForeignKey(
        TipoPromocion,
        on_delete=models.CASCADE,
        db_column='id_tipo_promocion',
        related_name='promociones',
    )

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"

    class Meta:
        db_table = 'promociones'
        indexes = [
            models.Index(fields=['estado'], name='idx_promociones_estado'),
            models.Index(fields=['id_categoria'], name='idx_promociones_categoria'),
            models.Index(fields=['id_supermercado'], name='idx_promociones_supermercado'),
            models.Index(fields=['id_usuario'], name='idx_promociones_usuario'),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(precio__gte=0),
                name='chk_promocion_precio_no_negativo',
            ),
            models.CheckConstraint(
                check=Q(descuento__isnull=True) | Q(descuento__gte=0, descuento__lte=100),
                name='chk_promocion_descuento_rango',
            ),
            models.CheckConstraint(
                check=Q(vistas__gte=0),
                name='chk_promocion_vistas_no_negativas',
            ),
            models.CheckConstraint(
                check=(
                    Q(fecha_fin__isnull=True)
                    | Q(fecha_inicio__isnull=True)
                    | Q(fecha_fin__gte=models.F('fecha_inicio'))
                ),
                name='chk_fechas_promocion',
            ),
        ]


class PromocionHorario(models.Model):
    DIA_SEMANA_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miercoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sabado'),
        ('domingo', 'Domingo'),
    ]

    id = models.BigAutoField(primary_key=True)
    dia_semana = models.CharField(max_length=15, choices=DIA_SEMANA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    codigo_promocion = models.ForeignKey(
        Promocion,
        on_delete=models.CASCADE,
        db_column='codigo_promocion',
        related_name='horarios',
    )

    def __str__(self):
        return (
            f"{self.codigo_promocion_id} - {self.dia_semana}: "
            f"{self.hora_inicio} a {self.hora_fin}"
        )

    class Meta:
        db_table = 'promociones_horarios'
        indexes = [
            models.Index(fields=['codigo_promocion'], name='idx_horarios_promocion'),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(hora_fin__gt=models.F('hora_inicio')),
                name='chk_horario_rango',
            ),
        ]
