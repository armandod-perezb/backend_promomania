from core.views import BaseModelViewSet

from .models import Reporte
from .serializers import ReporteSerializer


class ReporteViewSet(BaseModelViewSet):
    model = Reporte
    serializer_class = ReporteSerializer
