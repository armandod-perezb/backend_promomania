from django.db import models


class Notificacion(models.Model):
	TIPO_NOTIFICACION_CHOICES = [
		('action_executer', 'Action Executer'),
		('action_receiver', 'Action Receiver'),
		('action_controller', 'Action Controller'),
	]

	id = models.AutoField(primary_key=True)
	mensaje = models.CharField(max_length=255)
	fecha = models.DateTimeField(auto_now_add=True)
	t_notificacion = models.CharField(
		max_length=30,
		choices=TIPO_NOTIFICACION_CHOICES,
		default='action_receiver',
	)

	def __str__(self):
		return f"{self.t_notificacion}: {self.mensaje}"

	class Meta:
		db_table = 'Notificacion'
