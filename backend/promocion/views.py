from core.views import BaseModelViewSet
from django.db import transaction

from .models import Promocion, PromocionHorario, TipoPromocion
from .serializers import PromocionHorarioSerializer, PromocionSerializer, TipoPromocionSerializer
from .services import PromocionQueryService


promocion_query_service = PromocionQueryService()
PUNTOS_POR_PROMOCION_APROBADA = 100


class TipoPromocionViewSet(BaseModelViewSet):
    model = TipoPromocion
    serializer_class = TipoPromocionSerializer


class PromocionViewSet(BaseModelViewSet):
    model = Promocion
    serializer_class = PromocionSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        categoria_id = query_params.get('categoria_id')
        supermercado_id = query_params.get('supermercado_id')
        usuario_id = query_params.get('usuario_id')

        return promocion_query_service.get_filtered(
            estado=query_params.get('estado'),
            categoria_id=int(categoria_id) if categoria_id and categoria_id.isdigit() else None,
            supermercado_id=(
                int(supermercado_id)
                if supermercado_id and supermercado_id.isdigit()
                else None
            ),
            usuario_id=int(usuario_id) if usuario_id and usuario_id.isdigit() else None,
            term=query_params.get('q'),
        )

    @transaction.atomic
    def perform_update(self, serializer):
        promocion = serializer.save()

        if promocion.estado != 'aprobada' or promocion.puntuacion_otorgada:
            return

        usuario = promocion.id_usuario
        if usuario.rol != 'usuario':
            return

        usuario.agregar_puntuacion(PUNTOS_POR_PROMOCION_APROBADA)
        usuario.save(update_fields=['puntuacion', 'nivel', 'updated_at'])

        promocion.puntuacion_otorgada = True
        promocion.save(update_fields=['puntuacion_otorgada', 'updated_at'])


class PromocionHorarioViewSet(BaseModelViewSet):
    model = PromocionHorario
    serializer_class = PromocionHorarioSerializer
