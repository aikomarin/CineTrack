from rest_framework import serializers
from .models import SeriePelicula


class SeriePeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriePelicula
        fields = '__all__'
