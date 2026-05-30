from django.db import models
from promocion.models import Promocion
from usuario.models import Usuario


class Favorito(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
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

    def __str__(self):
        return f"Favorito {self.id_usuario_id} - {self.codigo_promocion_id}"

    class Meta:
        db_table = 'favoritos'
        indexes = [
            models.Index(fields=['id_usuario'], name='idx_favoritos_usuario'),
            models.Index(fields=['codigo_promocion'], name='idx_favoritos_promocion'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['id_usuario', 'codigo_promocion'],
                name='uq_favorito_usuario_promocion',
            ),
        ]
