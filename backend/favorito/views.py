from core.views import BaseModelViewSet

from .models import Favorito
from .serializers import FavoritoSerializer


class FavoritoViewSet(BaseModelViewSet):
    model = Favorito
    serializer_class = FavoritoSerializer
