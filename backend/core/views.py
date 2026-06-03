from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated


class BaseModelViewSet(viewsets.ModelViewSet):
    """Common ViewSet base for CRUD endpoints wired by DRF routers.

    Permite acceso de lectura público (list, retrieve) y requiere
    autenticación para operaciones de escritura (create, update, delete).
    """

    model = None

    def get_permissions(self):
        # Acciones de lectura son públicas
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        # Acciones de escritura requieren autenticación
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.model is None:
            raise ImproperlyConfigured(
                f'{self.__class__.__name__} requires a model attribute.'
            )
        return self.model.objects.all()