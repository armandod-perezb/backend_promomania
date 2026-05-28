from core.views import BaseModelViewSet

from .models import Supermercado
from .serializers import SupermercadoSerializer


class SupermercadoViewSet(BaseModelViewSet):
    model = Supermercado
    serializer_class = SupermercadoSerializer
