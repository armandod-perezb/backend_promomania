from core.views import BaseModelViewSet

from .models import Valoracion
from .serializers import ValoracionSerializer


class ValoracionViewSet(BaseModelViewSet):
    model = Valoracion
    serializer_class = ValoracionSerializer
