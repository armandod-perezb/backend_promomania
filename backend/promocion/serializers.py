from rest_framework import serializers

from .models import Promocion, PromocionHorario, TipoPromocion
from .services import PromocionValidationService


class TipoPromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPromocion
        fields = '__all__'


class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = '__all__'

    def validate(self, attrs):
        attrs = self._normalize_location_fields(attrs)
        instance = getattr(self, 'instance', None)
        merged = {}
        if instance is not None:
            # Keep current values when PATCH omits a field.
            merged = {
                'precio': instance.precio,
                'descuento': instance.descuento,
                'tipo_vigencia': instance.tipo_vigencia,
                'fecha_inicio': instance.fecha_inicio,
                'fecha_fin': instance.fecha_fin,
            }
        merged.update(attrs)
        PromocionValidationService.validate_business_rules(merged)
        return attrs

    def _normalize_location_fields(self, attrs: dict) -> dict:
        """
        Keep location mode consistent on partial updates:
        - If only physical location is provided, clear virtual URL.
        - If only virtual URL is provided, clear physical location + map coords.
        - Convert blank strings to null for optional text fields.
        """
        normalized = dict(attrs)

        if normalized.get('ubicacion') == '':
            normalized['ubicacion'] = None
        if normalized.get('url') == '':
            normalized['url'] = None

        has_ubicacion_key = 'ubicacion' in normalized
        has_url_key = 'url' in normalized

        if has_ubicacion_key and not has_url_key and normalized.get('ubicacion') is not None:
            normalized['url'] = None

        if has_url_key and not has_ubicacion_key and normalized.get('url') is not None:
            normalized['ubicacion'] = None
            normalized['lat'] = None
            normalized['lng'] = None

        if has_ubicacion_key and has_url_key:
            if normalized.get('ubicacion') is None and normalized.get('url') is not None:
                normalized['lat'] = None
                normalized['lng'] = None

        return normalized


class PromocionHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromocionHorario
        fields = '__all__'
