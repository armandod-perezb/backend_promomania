from django.db import models
from categoria.models import Categoria
from supermercado.models import Supermercado
from usuario.models import Usuario


class TipoPromocion(models.Model):
	ESTADO_CHOICES = [
		('activo', 'Activo'),
		('inactivo', 'Inactivo'),
	]

	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=255, null=True, blank=True)
	estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'TipoPromocion'


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

	codigo = models.CharField(max_length=50, primary_key=True)
	titulo = models.CharField(max_length=500)
	descripcion = models.TextField(null=True, blank=True)
	precio = models.DecimalField(max_digits=10, decimal_places=2)
	descuento = models.IntegerField(null=True, blank=True)
	condicion_producto = models.CharField(
		max_length=20,
		choices=CONDICION_PRODUCTO_CHOICES,
		default='nuevo',
	)
	ubicacion = models.CharField(max_length=255, null=True, blank=True)
	url = models.CharField(max_length=255, null=True, blank=True)
	foto = models.CharField(max_length=255, null=True, blank=True)
	tipo_vigencia = models.CharField(
		max_length=20,
		choices=TIPO_VIGENCIA_CHOICES,
		default='por_fecha',
	)
	fecha_inicio = models.DateField(null=True, blank=True)
	fecha_fin = models.DateField(null=True, blank=True)
	estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
	vistas = models.IntegerField(default=0)

	id_usuario = models.ForeignKey(
		Usuario,
		on_delete=models.CASCADE,
		db_column='id_usuario',
		related_name='promociones',
		null=True,
		blank=True,
	)
	id_supermercado = models.ForeignKey(
		Supermercado,
		on_delete=models.CASCADE,
		db_column='id_supermercado',
		related_name='promociones',
		null=True,
		blank=True,
	)
	id_categoria = models.ForeignKey(
		Categoria,
		on_delete=models.CASCADE,
		db_column='id_categoria',
		related_name='promociones',
		null=True,
		blank=True,
	)
	id_tipo_promocion = models.ForeignKey(
		TipoPromocion,
		on_delete=models.CASCADE,
		db_column='id_tipo_promocion',
		related_name='promociones',
		null=True,
		blank=True,
	)

	def __str__(self):
		return f"{self.codigo} - {self.titulo}"

	class Meta:
		db_table = 'Promocion'


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

	id = models.AutoField(primary_key=True)
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
		db_table = 'PromocionHorario'
