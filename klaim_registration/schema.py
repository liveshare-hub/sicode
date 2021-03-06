from django.db.models.query_utils import Q
import graphene
from graphene_django import DjangoObjectType
from .models import KPJ, DataTK
# from django.db.models import Q


class KPJType(DjangoObjectType):
    class Meta:
        model = KPJ


class DataTKType(DjangoObjectType):
    class Meta:
        model = DataTK
        fields = ("id", "nama", "nik")


class Query(graphene.ObjectType):
    all_kpjs = graphene.List(KPJType, no_kpj=graphene.String())
    all_tk = graphene.List(DataTKType, nik=graphene.String())

    def resolve_all_kpjs(root, info, no_kpj):

        if info.context.user.is_authenticated or info.context.user.is_superuser:
            return KPJ.objects.select_related('data_tk').filter(no_kpj=no_kpj, data_tk__hrd_id=info.context.user.pk)
        else:
            return KPJ.objects.none

    def resolve_all_tk(root, info, nik):
        if info.context.user.is_authenticated or info.context.user.is_superuser:
            return DataTK.objects.select_related('hrd').filter(nik=nik, hrd_id=info.context.user.pk)
        else:
            return KPJ.objects.none


schema = graphene.Schema(query=Query)
