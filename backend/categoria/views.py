from core.views import BaseModelViewSet

from .models import Categoria
from .serializers import CategoriaSerializer


class CategoriaViewSet(BaseModelViewSet):
    model = Categoria
    serializer_class = CategoriaSerializer
