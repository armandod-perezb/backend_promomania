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


class PromocionHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromocionHorario
        fields = '__all__'
