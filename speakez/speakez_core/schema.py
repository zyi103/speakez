import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.debug import DjangoDebug
from .models import Refugee

class RefugeeType(DjangoObjectType):
    class Meta:
        model = Refugee

class Query(graphene.ObjectType):
    all_refugees = graphene.List(RefugeeType)
    debug = graphene.Field(DjangoDebug, name='__debug')

    def resolve_all_refugees(self, info, **kwargs):
        return Refugee.objects.all()