from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Usuario
from .services import UsuarioValidationService


usuario_validation_service = UsuarioValidationService()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_correo(self, value):
        instance = getattr(self, 'instance', None)
        exclude_id = instance.id if instance else None
        usuario_validation_service.validate_correo_unico(value, exclude_id=exclude_id)
        return value.strip().lower()

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                'La contraseña debe tener al menos 8 caracteres.'
            )
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class AuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    usuario = UsuarioSerializer()
