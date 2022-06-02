import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from accounts.models import CustomUser
from .serializers import ProfileSerializer
from .grapheneTypes import ProfileType

class UpdateProfile(graphene.Mutation):
    msg = graphene.String()
    profile = graphene.Field(ProfileType)
    status=graphene.Int()
    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String()
        first_name= graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        # avatar = Upload()

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        try:
            profile = CustomUser.objects.get(pk=id)
            serializer = ProfileSerializer(profile, data=kwargs, partial=True)
            if profile != info.context.user:
                obj=None
                msg = "You aren't authorized to update other's Profiles."
            elif serializer.is_valid():
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