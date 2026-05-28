from django.db import models
from promocion.models import Promocion
from usuario.models import Usuario


class Comentario(models.Model):
	id = models.AutoField(primary_key=True)
	contenido = models.TextField()
	fecha = models.DateTimeField(auto_now_add=True)

	id_usuario = models.ForeignKey(
		Usuario,
		on_delete=models.CASCADE,
		db_column='id_usuario',
		related_name='comentarios',
		null=True,
		blank=True,
	)
	codigo_promocion = models.ForeignKey(
		Promocion,
		on_delete=models.CASCADE,
		db_column='codigo_promocion',
		related_name='comentarios',
		null=True,
		blank=True,
	)
	id_comment_reply = models.ForeignKey(
		'self',
		on_delete=models.CASCADE,
		db_column='id_comment_reply',
		related_name='respuestas',
		null=True,
		blank=True,
	)

	def __str__(self):
		return f"Comentario {self.id}"

	class Meta:
		db_table = 'Comentario'
