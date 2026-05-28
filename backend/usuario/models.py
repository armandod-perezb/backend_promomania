from django.db import models


class Usuario(models.Model):
    ROL_CHOICES = [
        ('usuario', 'Usuario'),
        ('admin', 'Admin'),
    ]

    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='usuario')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return self.estado == 'activo'

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

    class Meta:
        db_table = 'Usuario'


class UsuarioNotificacion(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='usuario_notificaciones',
    )
    id_notificacion = models.ForeignKey(
        'notificacion.Notificacion',
        on_delete=models.CASCADE,
        db_column='id_notificacion',
        related_name='usuario_notificaciones',
    )
    leida = models.BooleanField(default=False)
    fecha_recibida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Usuario {self.id_usuario_id} - "
            f"Notificacion {self.id_notificacion_id} - "
            f"Leida: {self.leida}"
        )

    class Meta:
        db_table = 'UsuarioNotificacion'
        unique_together = ('id_usuario', 'id_notificacion')
