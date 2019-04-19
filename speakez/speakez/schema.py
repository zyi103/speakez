import graphene
import speakez_core.schema

class Query(speakez_core.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)