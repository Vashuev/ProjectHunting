import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from accounts.models import CustomUser
from .serializers import ProfileSerializer
from .grapheneTypes import ProfileType
from core.settings import MEDIA_URL, BASE_DIR
import os

from mprs.decorators import login_required

class UpdateProfile(graphene.Mutation):
    message = graphene.String()
    profile = graphene.Field(ProfileType)
    error=graphene.Boolean()
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        avatars = graphene.List(Upload)

    @classmethod
    @login_required
    def mutate(cls, root, info, username, email, avatars):
        try:
            profile = CustomUser.objects.get(pk=info.context.user.id)
            last_path = str(BASE_DIR) + str(MEDIA_URL) + str(profile.avatar)
            print(last_path)
            data = {
                'username' : username,
                'email' : email
            }
            if len(avatars):
                data['avatar'] = avatars[0]
            serializer = ProfileSerializer(instance=profile, data=data, partial=True)
            if serializer.is_valid():
                obj = serializer.save()
                logo_name = last_path.split('/')[-1]
                if logo_name != 'default.jpg':
                    try:
                        os.remove(last_path)
                    except:
                        print("last avatar file doesn't exist on server")
                msg = "Updated"
                error = False
            else:
                msg = serializer.errors
                obj = None
                error = True
            return cls(profile=obj, message=msg, error = error)
        except:
            return cls(profile=None, message="<Profile : {}> doesn't exist".format(id), error=True)

    
class AccountMutation(graphene.ObjectType):
    update_Profile = UpdateProfile.Field()