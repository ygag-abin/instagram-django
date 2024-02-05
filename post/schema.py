"""
import graphene
from graphene_django.types import DjangoObjectType
from post.models import Post, Like, Comment
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    all_likes = graphene.List(LikeType)
    all_comments = graphene.List(CommentType)

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_all_likes(self, info, **kwargs):
        return Like.objects.all()

    def resolve_all_comments(self, info, **kwargs):
        return Comment.objects.all()


schema = graphene.Schema(query=Query)
"""

import graphene
from graphene_django.types import DjangoObjectType
from .models import Post
from django.contrib.auth.models import User
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = User


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()


class CreatePostMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        image = graphene.String(required=True)
        caption = graphene.String(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, user_id, image, caption):
        user = User.objects.get(pk=user_id)
        post = Post(user=user, image=image, caption=caption)
        post.save()
        return CreatePostMutation(post=post)


class UpdatePostMutation(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        image = graphene.String()
        caption = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, post_id, **kwargs):
        post = Post.objects.get(pk=post_id)
        for field, value in kwargs.items():
            setattr(post, field, value)
        post.save()
        return UpdatePostMutation(post=post)


class DeletePostMutation(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            post.delete()
            success = True
        except Post.DoesNotExist:
            success = False
        return DeletePostMutation(success=success)


class Mutation(AuthMutation, graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    update_post = UpdatePostMutation.Field()
    delete_post = DeletePostMutation.Field()


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)

    def resolve_all_posts(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user


schema = graphene.Schema(query=Query, mutation=Mutation)
