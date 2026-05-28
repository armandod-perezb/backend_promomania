from django.db import models
from promocion.models import Promocion
from usuario.models import Usuario


class Favorito(models.Model):
	id = models.AutoField(primary_key=True)
	id_usuario = models.ForeignKey(
		Usuario,
		on_delete=models.CASCADE,
		db_column='id_usuario',
		related_name='favoritos',
	)
	codigo_promocion = models.ForeignKey(
		Promocion,
		on_delete=models.CASCADE,
		db_column='codigo_promocion',
		related_name='favoritos',
	)
	fecha = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Favorito {self.id_usuario_id} - {self.codigo_promocion_id}"

	class Meta:
		db_table = 'Favorito'
		unique_together = ('id_usuario', 'codigo_promocion')
