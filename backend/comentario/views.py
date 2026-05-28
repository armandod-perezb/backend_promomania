from core.views import BaseModelViewSet

from .models import Comentario
from .serializers import ComentarioSerializer


class ComentarioViewSet(BaseModelViewSet):
    model = Comentario
    serializer_class = ComentarioSerializer
