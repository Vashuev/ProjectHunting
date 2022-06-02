
import graphene
from .grapheneTypes import ProfileType
from accounts.models import CustomUser

class AccountQuery(graphene.ObjectType):
    message = graphene.String()
    profile = graphene.Field(ProfileType, id=graphene.ID(required=True))
    status = graphene.Int()
    def resolve_profile(root, info, id=None):
        try:
            profile = CustomUser.objects.get(pk=id)
            if profile != info.context.user:
                message = "You are not authorized to access others profile"
            else:
                message = "Accepted"
            status = 200
            return {message : message, profile: None, status: status}
        except:
            message = "<profile : {}> doesn't exits".format(id)
            status = 400
            return {message : message, profile: None, status:status}