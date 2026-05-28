from django.db import models
from promocion.models import Promocion
from usuario.models import Usuario

class Valoracion(models.Model):
	TIPO_CHOICES = [
		('positiva', 'Positiva'),
		('negativa', 'Negativa'),
	]

	id = models.AutoField(primary_key=True)
	tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

	id_usuario = models.ForeignKey(
		Usuario,
		on_delete=models.CASCADE,
		db_column='id_usuario',
		related_name='valoraciones',
		null=True,
		blank=True,
	)
	codigo_promocion = models.ForeignKey(
		Promocion,
		on_delete=models.CASCADE,
		db_column='codigo_promocion',
		related_name='valoraciones',
		null=True,
		blank=True,
	)

	def __str__(self):
		return f"Valoracion {self.id} - {self.tipo}"

	class Meta:
		db_table = 'Valoracion'
		unique_together = ('id_usuario', 'codigo_promocion')
