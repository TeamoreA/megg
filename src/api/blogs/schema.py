import graphene
from graphene_django import DjangoObjectType

from .models import Blog as BlogModel
from utilities.validations import validate_empty_fields


class Blog(DjangoObjectType):
    class Meta:
        model = BlogModel


class CreateBlog(graphene.Mutation):
    """Mutation to create a blog"""
    blog = graphene.Field(Blog)

    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        picture = graphene.String()

    def mutate(self, info, **kwargs):
        validate_empty_fields(**kwargs)
        author = info.context.user
        blog = BlogModel(
            title=kwargs.get('title'),
            body=kwargs.get('body'),
            picture=kwargs.get('picture'),
            author=author
        )
        blog.save()

        return CreateBlog(blog=blog)


class Mutation(graphene.ObjectType):
    create_blog = CreateBlog.Field(
        description="Creates a new user with the arguments below."
        )


class Query(graphene.ObjectType):
    """Blogs query"""
    blogs = graphene.List(
        Blog,
        first=graphene.Int(),
        skip=graphene.Int()
    )

    def resolve_blogs(self, info, **kwargs):
        blogs_query = BlogModel.objects.all()
        first = kwargs.get('first')
        skip = kwargs.get('skip')

        if first:
            # slice the blogs_query list
            blogs_query = blogs_query[:first]

        if skip:
            # slice the blogs_query list
            blogs_query = blogs_query[skip:]

        return blogs_query
