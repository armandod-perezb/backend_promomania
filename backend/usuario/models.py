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

    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    correo = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=120, null=True, blank=True)
    nivel = models.IntegerField(null=True, blank=True)
    puntuacion = models.IntegerField(null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='usuario')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        db_table = 'usuarios'
