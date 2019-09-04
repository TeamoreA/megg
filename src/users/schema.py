# users schema
from .models import CustomUser

import graphene
from graphene_django import DjangoObjectType


class User(DjangoObjectType):
    class Meta:
        model = CustomUser
        interfaces = (graphene.Node, )

class User_Connection(graphene.Connection):
    class Meta:
        node = User
    count = graphene.Int()

    def resolve_count(self, info):
        return len(self.edges)


class CreateUser(graphene.Mutation):
    """Mutation to create a new user"""
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()

    def mutate(self, info, **kwargs):
        user = CustomUser(
            username=kwargs.get('username'),
            email=kwargs.get('email'),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name')
        )
        user.set_password(kwargs.get('password'))
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field(description="Creates a new user with the arguments below.")


class Query(graphene.ObjectType):
    users = graphene.ConnectionField(User_Connection)

    def resolve_users(self, info, **kwargs):
        return CustomUser.objects.all()