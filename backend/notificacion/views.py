from core.views import BaseModelViewSet

from .models import Notificacion
from .serializers import NotificacionSerializer


class NotificacionViewSet(BaseModelViewSet):
    model = Notificacion
    serializer_class = NotificacionSerializer
