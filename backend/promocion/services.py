from __future__ import annotations

from rest_framework.exceptions import ValidationError

from .repositories import PromocionRepository


class PromocionQueryService:
    def __init__(self, repository: PromocionRepository | None = None):
        self.repository = repository or PromocionRepository()

    def get_filtered(
        self,
        *,
        estado: str | None = None,
        categoria_id: int | None = None,
        supermercado_id: int | None = None,
        usuario_id: int | None = None,
        term: str | None = None,
    ):
        return self.repository.filter_queryset(
            estado=estado,
            categoria_id=categoria_id,
            supermercado_id=supermercado_id,
            usuario_id=usuario_id,
            term=term,
        )


class PromocionValidationService:
    @staticmethod
    def validate_business_rules(attrs: dict):
        precio = attrs.get('precio')
        descuento = attrs.get('descuento')
        tipo_vigencia = attrs.get('tipo_vigencia')
        fecha_inicio = attrs.get('fecha_inicio')
        fecha_fin = attrs.get('fecha_fin')

        errors = {}

        if precio is not None and precio <= 0:
            errors['precio'] = 'El precio debe ser mayor a 0.'

        if descuento is not None and not (0 <= descuento <= 100):
            errors['descuento'] = 'El descuento debe estar entre 0 y 100.'

        if tipo_vigencia == 'por_fecha':
            if not fecha_inicio or not fecha_fin:
                errors['tipo_vigencia'] = (
                    'Para vigencia por fecha se requieren fecha_inicio y fecha_fin.'
                )
            elif fecha_inicio > fecha_fin:
                errors['fecha_fin'] = (
                    'La fecha de fin no puede ser menor a la fecha de inicio.'
                )

        if tipo_vigencia == 'permanente' and fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            errors['fecha_fin'] = (
                'Si envias fechas en vigencia permanente, fecha_fin debe ser mayor o igual a fecha_inicio.'
            )

        if errors:
            raise ValidationError(errors)
