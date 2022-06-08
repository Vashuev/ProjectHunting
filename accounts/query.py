
import graphene
from .grapheneTypes import ProfileType
from accounts.models import CustomUser
from .serializers import ProfileSerializer

class AccountQuery(graphene.ObjectType):
    get_profile = graphene.Field(ProfileType, id=graphene.Int())

    def resolve_get_profile(root, info, id=-1):
        try:
            if id != -1:
                profile = CustomUser.objects.get(pk=id)
                profile.avatar = info.context.build_absolute_uri(profile.avatar.url)
            elif info.context.user.is_authenticated:
                profile = CustomUser.objects.get(pk=info.context.user.id)
                profile.avatar = info.context.build_absolute_uri(profile.avatar.url)
            else:
                profile = None
            return profile
        except:
            return None