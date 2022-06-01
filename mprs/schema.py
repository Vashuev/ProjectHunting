from .mutations import AllMutation as mutation
from .graphenetype import UserType, TagType, CommentType, ProjectType, ScreenshotType, ReplyType
from .models import TagModel, CommentModel, ProjectModel, ScreenshotModel, ReplyModel
import graphene

class Query(graphene.ObjectType):
    all_project = graphene.List(ProjectType)
    all_tag = graphene.List(TagType)
    def resolve_all_project(root, info):
        return ProjectModel.objects.all()

    def resolve_all_tag(root, info):
        return TagModel.objects.all()

    project_by_id = graphene.Field(ProjectType, id=graphene.ID())
    def resolve_project_by_id(root, info, id):
        try:
            return ProjectModel.objects.get(pk=id)
        except ProjectModel.DoesNotExist:
            return None
    
    project_by_tagid = graphene.Field(TagType, id=graphene.ID())
    def resolve_project_by_tagid(root, info, id):
        try:
            return TagModel.objects.get(pk=id)
        except  TagModel.DoesNotExist:
            return None

schema = graphene.Schema(query=Query, mutation=mutation)
