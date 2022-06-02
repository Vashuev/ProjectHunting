from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from .models import TagModel, CommentModel, ProjectModel, ScreenshotModel, ReplyModel

class UserType(DjangoObjectType): 
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'username', 'email']

class TagType(DjangoObjectType):
    class Meta:
        model = TagModel
        fields = '__all__'

class ProjectType(DjangoObjectType):
    class Meta:
        model = ProjectModel
        fields = '__all__'


class ScreenshotType(DjangoObjectType):
    class Meta:
        model = ScreenshotModel
        fields = '__all__'

class CommentType(DjangoObjectType):
    class Meta:
        model = CommentModel
        fields = '__all__'

class ReplyType(DjangoObjectType):
    class Meta:
        model = ReplyModel
        fields = '__all__'