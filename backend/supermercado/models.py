from django.db import models


class Supermercado(models.Model):
	ESTADO_CHOICES = [
		('activo', 'Activo'),
		('inactivo', 'Inactivo'),
	]

	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=150)
	direccion = models.CharField(max_length=255, null=True, blank=True)
	ciudad = models.CharField(max_length=100, null=True, blank=True)
	estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

	def __str__(self):
		return f"{self.nombre} ({self.estado})"

	class Meta:
		db_table = 'Supermercado'
