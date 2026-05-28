from __future__ import annotations

from django.db.models import Q, QuerySet

from .models import Promocion


class PromocionRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Promocion]:
        return (
            Promocion.objects.select_related(
                'id_usuario',
                'id_supermercado',
                'id_categoria',
                'id_tipo_promocion',
            )
            .all()
            .order_by('-fecha_inicio', 'codigo')
        )

    @staticmethod
    def filter_queryset(
        *,
        estado: str | None = None,
        categoria_id: int | None = None,
        supermercado_id: int | None = None,
        usuario_id: int | None = None,
        term: str | None = None,
    ) -> QuerySet[Promocion]:
        qs = PromocionRepository.get_queryset()
        if estado:
            qs = qs.filter(estado=estado)
        if categoria_id:
            qs = qs.filter(id_categoria_id=categoria_id)
        if supermercado_id:
            qs = qs.filter(id_supermercado_id=supermercado_id)
        if usuario_id:
            qs = qs.filter(id_usuario_id=usuario_id)
        if term:
            qs = qs.filter(
                Q(titulo__icontains=term)
                | Q(descripcion__icontains=term)
                | Q(ubicacion__icontains=term)
            )
        return qs
