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

    votedByMe = graphene.Boolean()
    logoUrl = graphene.String()
    
    def resolve_votedByMe(self, info):
        if info.context.user.is_authenticated:
            curr_voter = get_user_model().objects.get(pk=info.context.user.id)
            all_voters = self.votedBy.all()
            if curr_voter in all_voters:
                return True
        return False

    def resolve_logoUrl(self, info):
        return info.context.build_absolute_uri(self.logo.url)

class ScreenshotType(DjangoObjectType):
    class Meta:
        model = ScreenshotModel
        fields = '__all__'

    screenshotUrl = graphene.String()
    def resolve_screenshotUrl(self, info):
        return info.context.build_absolute_uri(self.image.url)

class CommentType(DjangoObjectType):
    class Meta:
        model = CommentModel
        fields = '__all__'

class ReplyType(DjangoObjectType):
    class Meta:
        model = ReplyModel
        fields = '__all__'