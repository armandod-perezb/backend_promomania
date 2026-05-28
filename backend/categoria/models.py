from django.db import models


class Categoria(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'Categoria'
