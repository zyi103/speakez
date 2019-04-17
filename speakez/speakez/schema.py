import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.debug import DjangoDebug

class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query)