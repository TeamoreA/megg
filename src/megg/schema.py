
import graphene
import graphql_jwt

# local imports
import api.users.schema
import api.blogs.schema
import api.likes.schema


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(api.users.schema.User)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Query(
    api.users.schema.Query,
    api.blogs.schema.Query,
    api.likes.schema.Query,
    graphene.ObjectType
    ):
    """The base query class"""
    pass


class Mutation(
    api.users.schema.Mutation,
    api.blogs.schema.Mutation,
    api.likes.schema.Mutation,
    graphene.ObjectType
    ):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
