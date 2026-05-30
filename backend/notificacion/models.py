from django.db import models
from usuario.models import Usuario


class Notificacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=40, default='general')
    id_usuario_destino = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        db_column='id_usuario_destino',
        related_name='notificaciones_destino',
        null=True,
        blank=True,
    )
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo}: {self.mensaje}"

    class Meta:
        db_table = 'notificaciones'
        indexes = [
            models.Index(fields=['id_usuario_destino'], name='idx_notificaciones_usuario'),
            models.Index(fields=['leida'], name='idx_notificaciones_leida'),
        ]
