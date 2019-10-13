import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

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

    @login_required
    def mutate(self, info, **kwargs):
        validate_empty_fields(**kwargs)
        blog_id = kwargs.get('blog_id')
        author = info.context.user
        blog = Blog.objects.filter(id=blog_id).first()
        comment = CommentsModel(
            author=author,
            body=kwargs.get('body'),
            blog=blog
        )
        comment.save()

        return CreateComment(comment=comment)

class UpdateComment(graphene.Mutation):
    """class to update a comment"""
    comment = graphene.Field(Comment)

    class Arguments:
        comment_id = graphene.Int(required=True)
        body = graphene.String(required=True)
    @login_required
    def mutate(self, info, **kwargs):
        validate_empty_fields(**kwargs)
        comment_id = kwargs.get('comment_id')
        author = info.context.user
        comment = CommentsModel.objects.filter(id=comment_id).first()
        if comment.author_id != author.id:
            raise GraphQLError('Permission denied, You cannot delete this comment')
        comment.body=kwargs.get('body')
        comment.save()
        return UpdateComment(comment=comment)

class DeleteComment(graphene.Mutation):
    comment = graphene.Field(Comment)

    class Arguments:
        comment_id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, comment_id):
        author = info.context.user
        comment = CommentsModel.objects.filter(id=comment_id).first()
        if comment.author_id != author.id:
            raise GraphQLError('Permission denied, You cannot delete this comment')
        comment.delete()
        return DeleteComment(comment=comment)

class Mutation(graphene.ObjectType):
    comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()
    update_comment = UpdateComment.Field()

class Query(graphene.ObjectType):
    """Query for the list of comments of a specific blog"""
    comments = graphene.List(Comment, blog_id = graphene.Int(required=True))

    def resolve_comments(self, info, **kwargs):
        blog_id = kwargs.get('blog_id')
        comments = CommentsModel.objects.filter(blog_id=blog_id)
        return comments