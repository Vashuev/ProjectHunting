from .graphenetype import UserType, TagType, CommentType, ProjectType, ScreenshotType, ReplyType
from .models import TagModel, CommentModel, ProjectModel, ScreenshotModel, ReplyModel
import graphene
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .decorators import login_required
from .serializers import ProjectSerializer

class MprsQuery(graphene.ObjectType):
    all_project = graphene.List(ProjectType)

    def resolve_all_project(root, info, message=None):
        instances = ProjectModel.objects.all()
        for intance in instances:
            if intance.logo:
                intance.logo = info.context.build_absolute_uri(intance.logo.url)
        return instances

    all_tag = graphene.List(TagType)
    def resolve_all_tag(root, info):
        return TagModel.objects.all()

    filter_tag = graphene.List(TagType, tag_name=graphene.String())
    def resolve_filter_tag(root, info, tag_name):
        return TagModel.objects.filter(tag_name__contains=tag_name)

    filter_project = graphene.List(ProjectType, text_to_search=graphene.String())
    def resolve_filter_project(root, info, text_to_search):
        vector = SearchVector('name', 'subtitle', 'description')
        query = SearchQuery(text_to_search)
        return ProjectModel.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.01).order_by('-rank')

    project_by_id = graphene.Field(ProjectType, id=graphene.ID())
    def resolve_project_by_id(root, info, id): 
        try:
            project = ProjectModel.objects.get(pk=id)
            if project.logo:
                project.logo = info.context.build_absolute_uri(project.logo.url)
            return project
        except ProjectModel.DoesNotExist:
            return None
    
    project_by_tagid = graphene.Field(TagType, id=graphene.ID())
    def resolve_project_by_tagid(root, info, id):
        try:
            return TagModel.objects.get(pk=id)
        except  TagModel.DoesNotExist:
            return None


