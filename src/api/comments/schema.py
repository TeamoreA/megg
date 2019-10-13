import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from api.blogs.models import Blog
from api.users.models import CustomUser as User
from .models import Comments as CommentsModel
from utilities.validations import validate_empty_fields

class Comment(DjangoObjectType):
    class Meta:
        model = CommentsModel

class CreateComment(graphene.Mutation):
    comment = graphene.Field(Comment)

    class Arguments:
        blog_id = graphene.Int(required=True)
        body = graphene.String(required=True)
    def mutate(self, info, **kwargs):
        validate_empty_field(**kwargs)
        blog_id = kwargs.get('blog_id')
        author = info.context.user
        if author.is_anonymous:
            raise GraphQLError("Ensure you are logged in to perform this action")
        blog = Blog.objects.filter(blog_id=blog_id).first()
        comment = CommentsModel(
            author=author,
            body=kwargs.get('body'),
            blog=blog
        )
        comment.save()

        return CreateComment(comment=comment)

class Mutation(graphene.ObjectType):
    comment = CreateComment()