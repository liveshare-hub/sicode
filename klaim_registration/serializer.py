from rest_framework import serializers
from .models import KPJ


class KPJSerializer(serializers.ModelSerializer):
    data_tk = serializers.StringRelatedField(many=True)

    class Meta:
        model = KPJ
        fields = ['id', 'data_tk', 'no_kpj', 'data_tk']
