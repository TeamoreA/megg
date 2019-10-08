import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from api.blogs.models import Blog
from .models import Like as LikeModel
from api.users.models import CustomUser as User

class Like(DjangoObjectType):
    class Meta:
        model = LikeModel

class LikeBlog(graphene.Mutation):

    like = graphene.Field(Like)

    class Arguments:
        blog_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        blog_id = kwargs.get('blog_id')
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to perform this action!')
        blog = Blog.objects.filter(id=blog_id).first()
        if not blog:
            raise GraphQLError('Blog with that Id not found!')
        user_likes = LikeModel.objects.filter(blog_id=blog_id, user_id=user.id).first()
        if user_likes:
            user_likes.delete()
            like = LikeModel(
                user=user,
                blog=blog
            )
        else:
            like = LikeModel(
                user=user,
                blog=blog
            )
            like.save()

        return LikeBlog(like=like)

class Mutation(graphene.ObjectType):
    like_blog = LikeBlog.Field()

class Query(graphene.ObjectType):
    likes = graphene.List(Like, blog_id=graphene.Int())

    def resolve_likes(self, info, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog_likes = LikeModel.objects.filter(blog_id=blog_id)
        return blog_likes
