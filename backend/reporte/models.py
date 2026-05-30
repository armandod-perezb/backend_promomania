from django.db import models
from promocion.models import Promocion
from usuario.models import Usuario


class Reporte(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('revisado', 'Revisado'),
        ('descartado', 'Descartado'),
    ]

    id = models.BigAutoField(primary_key=True)
    motivo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='reportes',
    )
    codigo_promocion = models.ForeignKey(
        Promocion,
        on_delete=models.CASCADE,
        db_column='codigo_promocion',
        related_name='reportes',
    )

    def __str__(self):
        return f"Reporte {self.id} - {self.estado}"

    class Meta:
        db_table = 'reportes'
        indexes = [
            models.Index(fields=['estado'], name='idx_reportes_estado'),
            models.Index(fields=['codigo_promocion'], name='idx_reportes_promocion'),
        ]
