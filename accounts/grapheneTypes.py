import graphene
from graphene_django import DjangoObjectType

from accounts.models import CustomUser

class ProfileType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ['id', 'username','first_name', 'last_name', 'avatar', 'email',]

    avatarUrl = graphene.String()

    def resolve_avatarUrl(self, info):
        return info.context.build_absolute_uri(self.avatar.url)