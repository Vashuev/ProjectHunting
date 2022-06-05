import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from accounts.models import CustomUser
from .serializers import ProfileSerializer
from .grapheneTypes import ProfileType

from mprs.decorators import login_required

class UpdateProfile(graphene.Mutation):
    msg = graphene.String()
    profile = graphene.Field(ProfileType)
    status=graphene.Int()
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        avatar = Upload()

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        try:
            profile = CustomUser.objects.get(pk=info.context.user.id)
            serializer = ProfileSerializer(profile, data=kwargs, partial=True)
            if serializer.is_valid():
                obj = serializer.save()
                msg = "Updated"
            else:
                msg = serializer.errors
                obj = None
            return cls(profile=obj, msg=msg, status=200)
        except:
            return cls(profile=None, msg="<Profile : {}> doesn't exist".format(id), status=400)

    
class AccountMutation(graphene.ObjectType):
    update_Profile = UpdateProfile.Field()