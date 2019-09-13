# users schema
from graphql import GraphQLError
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import password_validation

from .models import CustomUser
from utilities.validations import (
    verify_email, validate_empty_fields
    )


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
        validate_empty_fields(**kwargs)
        password = kwargs.get('password')
        email = kwargs.get('email')
        password_validation.validate_password(password)
        if not verify_email(email):
            raise GraphQLError("The email format is invalid")
        user = CustomUser(
            username=kwargs.get('username'),
            email=email,
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name')
        )
        user.set_password(password)
        import pdb; pdb.set_trace()
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field(description="Creates a new user with the arguments below.")


class Query(graphene.ObjectType):
    users = graphene.ConnectionField(User_Connection)

    def resolve_users(self, info, **kwargs):
        return CustomUser.objects.all()