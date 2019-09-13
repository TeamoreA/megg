
import graphene

from api.users import schema

from graphene_django.debug import DjangoDebug


class Query(schema.Query, graphene.ObjectType):
    pass

class Mutation(schema.Mutation, graphene.ObjectType,):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)