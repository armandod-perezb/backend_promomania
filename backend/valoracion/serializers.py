from rest_framework import serializers

from .models import Valoracion


class ValoracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valoracion
        fields = '__all__'
