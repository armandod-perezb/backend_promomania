from django.db import models
from django.db.models import Q
from promocion.models import Promocion
from usuario.models import Usuario

class Valoracion(models.Model):
    TIPO_CHOICES = [
        ('positiva', 'Positiva'),
        ('negativa', 'Negativa'),
    ]

    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='valoraciones',
    )
    codigo_promocion = models.ForeignKey(
        Promocion,
        on_delete=models.CASCADE,
        db_column='codigo_promocion',
        related_name='valoraciones',
    )

    def __str__(self):
        return f"Valoracion {self.id} - {self.tipo}"

    class Meta:
        db_table = 'valoraciones'
        indexes = [
            models.Index(fields=['codigo_promocion'], name='idx_valoraciones_promocion'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['id_usuario', 'codigo_promocion'],
                name='uq_valoracion_usuario_promocion',
            ),
            models.CheckConstraint(
                check=Q(tipo__in=['positiva', 'negativa']),
                name='chk_tipo_valoracion',
            ),
        ]
