import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from api.blogs.models import Blog
from .models import DislikeModel
from .models import Like as LikeModel
from api.users.models import CustomUser as User

class Like(DjangoObjectType):
    class Meta:
        model = LikeModel

class Dislike(DjangoObjectType):
    class Meta:
        model = DislikeModel

class DislikeBlog(graphene.Mutation):
    dislike = graphene.Field(Dislike)

    class Arguments:
        blog_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        blog_id = kwargs.get('blog_id')
        user = info.context.user
        if not user:
            raise GraphQLError('You must be logged in to perform this action')

        blog = Blog.objects.filter(id=blog_id).first()
        if not blog:
            raise GraphQLError('Blog with that Id not found')
        user_dislike = DislikeModel.objects.filter(blog_id=blog_id, user_id=user.id).first()
        dislike = DislikeModel(
            blog=blog,
            user=user
        )
        if user_dislike:
            user_dislike.delete()
        else:
            dislike.save()
        return DislikeBlog(dislike=dislike)

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
        user_like = LikeModel.objects.filter(blog_id=blog_id, user_id=user.id).first()
        like = LikeModel(
                user=user,
                blog=blog
            )
        if user_like:
            user_like.delete()
        else:
            like.save()

        return LikeBlog(like=like)

class Mutation(graphene.ObjectType):
    like_blog = LikeBlog.Field()
    dislike_blog = DislikeBlog.Field()

class Query(graphene.ObjectType):
    likes = graphene.List(Like, blog_id=graphene.Int())
    dislikes = graphene.List(Dislike, blog_id=graphene.Int())

    def resolve_likes(self, info, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog_likes = LikeModel.objects.filter(blog_id=blog_id)
        return blog_likes

    def resolve_dislikes(self, info, **kwargs):
        blog_id = kwargs.get('blog_id')
        import pdb; pdb.set_trace()
        blog_dislikes = DislikeModel.objects.filter(blog_id=blog_id)
        return blog_dislikes
