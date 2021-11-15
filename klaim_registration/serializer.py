from rest_framework import serializers
from .models import KPJ, DataTK


class DataTKSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTK
        fields = ['id', 'nama']


class KPJSerializer(serializers.ModelSerializer):
    data_tk = DataTKSerializer(many=True, read_only=True)

    class Meta:
        model = KPJ
        fields = ['id', 'no_kpj', 'data_tk']
