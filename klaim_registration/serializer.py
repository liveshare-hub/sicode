from rest_framework import serializers
from .models import KPJ


class KPJSerializer(serializers.ModelSerializer):
    list_kpj = serializers.StringRelatedField(many=True)

    class Meta:
        model = KPJ
        fields = ['id', 'data_tk', 'no_kpj', 'list_kpj']
