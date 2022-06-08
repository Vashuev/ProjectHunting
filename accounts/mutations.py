from email import message
from ftplib import error_reply
from xmlrpc.client import Boolean
import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from accounts.models import CustomUser
from .serializers import ProfileSerializer
from .grapheneTypes import ProfileType

from mprs.decorators import login_required

class UpdateProfile(graphene.Mutation):
    message = graphene.String()
    profile = graphene.Field(ProfileType)
    error=graphene.Boolean()
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
                error = True
            else:
                msg = serializer.errors
                obj = None
                error = False
            return cls(profile=obj, message=msg, error = error)
        except:
            return cls(profile=None, message="<Profile : {}> doesn't exist".format(id), error=False)

    
class AccountMutation(graphene.ObjectType):
    update_Profile = UpdateProfile.Field()