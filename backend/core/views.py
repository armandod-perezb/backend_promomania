from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets


class BaseModelViewSet(viewsets.ModelViewSet):
    """Common ViewSet base for CRUD endpoints wired by DRF routers."""

    model = None

    def get_queryset(self):
        if self.model is None:
            raise ImproperlyConfigured(
                f'{self.__class__.__name__} requires a model attribute.'
            )
        return self.model.objects.all()