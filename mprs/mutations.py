from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from .models import TagModel, CommentModel, ProjectModel, ScreenshotModel, ReplyModel
from .graphenetype import UserType, TagType, CommentType, ProjectType, ScreenshotType, ReplyType
from graphene_file_upload.scalars import Upload
from django.db import transaction

class CommentUpdateMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()
    class Arguments:
        # The input arguments for this mutation
        comment = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    commentInstance = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, comment, id):
        try:
            commentInstance = CommentModel.objects.get(pk=id)
            if commentInstance.owner_id != info.context.user:
                return cls(response=False, message = "You are not the owner of this comment")
            commentInstance.comment = comment
            commentInstance.save()
            return CommentUpdateMutation(commentInstance=commentInstance)
        except CommentModel.DoesNotExist:
            return cls(response=False, message = "<Comment object > with id:{id} is not in database".format(id=id))

class ReplyUpdateMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()
    class Arguments:
        # The input arguments for this mutation
        reply = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    replyInstance = graphene.Field(ReplyType)

    @classmethod
    def mutate(cls, root, info, reply, id):
        try:
            replyInstance = ReplyModel.objects.get(pk=id)
            if replyInstance.owner_id != info.context.user:
                return cls(response=False, message = "You are not the owner of this reply")
            replyInstance.reply = reply
            replyInstance.save()
            return ReplyUpdateMutation(replyInstance=replyInstance)
        except ReplyModel.DoesNotExist:
            return cls(response=False, message = "<Reply object > with id:{id} is not in database".format(id=id))

class ProjectUpdateMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()

    projectInstance = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, id, name=None, subtitle=None, description=None):
        try:
            projectInstance = ProjectModel.objects.get(pk=id)
            if projectInstance.owner_id != info.context.user:
                return cls(response=False, message = "You are not the owner of this Project")
            if name!= None: 
                projectInstance.name = name
            if subtitle != None:
                projectInstance.subtitle = subtitle
            if description != None:
                projectInstance.description = description
            projectInstance.save()
            return ProjectUpdateMutation(projectInstance=projectInstance)
        except ProjectModel.DoesNotExist:
            return cls(response=False, message = "<Project object > with id:{id} is not in database".format(id=id))

class CommentDeleteMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            comment = CommentModel.objects.get(pk=id)
            if comment.owner_id != info.context.user:
                return cls(response=False, message = "You are not the owner of this comment")
            comment.delete()
            return cls(response=True, message="Comment Deleted")
        except CommentModel.DoesNotExist:
            return cls(response=False, message = "<Comment object > with id:{id} is not in database".format(id=id))

class ReplyDeleteMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            reply = ReplyModel.objects.get(pk=id)
            if reply.owner_id != info.context.user:
                return cls(response=False, message = "You are not the owner of this reply")
            reply.delete()
            return cls(response=True, message="reply Deleted")
        except ReplyModel.DoesNotExist:
            return cls(response=False, message = "<Reply object > with id:{id} is not in database".format(id=id))

class ProjectDeleteMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            project = ProjectModel.objects.get(pk=id)
            if project.owner_id != info.context.user:
                return cls(response=False, message = "You are not the owner of this Project")
            project.delete()
            return cls(response=True, message="Project Deleted")
        except ProjectModel.DoesNotExist:
            return cls(response=False, message = "<Project object > with id:{id} is not in database".format(id=id))

class ScreenshotDeleteMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            screenshot = ScreenshotModel.objects.get(pk=id)
            if screenshot.owner_id != info.context.user:
                return cls(response=False, message = "You are not the owner of this Screenshot")
            screenshot.delete()
            return cls(response=True, message="Screenshot Deleted")
        except ReplyModel.DoesNotExist:
            return cls(response=False, message = "<Screenshot object > with id:{id} is not in database".format(id=id))

class CommentCreateMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()
    commentInstance = graphene.Field(CommentType)

    class Arguments:
        id = graphene.ID()      # product id
        comment = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, id, comment):
        try:
            project = ProjectModel.objects.get(pk=id)
            commentInstance = CommentModel.objects.create(comment=comment, project_id = project, owner_id = info.context.user)
            commentInstance.save()
            return cls(commentInstance=commentInstance)
        except ProjectModel.DoesNotExist:
            return cls(response=False, message = "<Project object > with id:{id} is not in database".format(id=id))

class ReplyCreateMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()
    replyInstance = graphene.Field(ReplyType)

    class Arguments:
        id = graphene.ID()      # comment id
        reply = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, id, reply):
        try:
            comment = CommentModel.objects.get(pk=id)
            replyInstance = ReplyModel.objects.create(reply=reply,comment_id=comment, owner_id = info.context.user)
            replyInstance.save()
            return cls(replyInstance=replyInstance)
        except CommentModel.DoesNotExist:
            return cls(response=False, message = "<Comment object > with id:{id} is not in database".format(id=id))


def createAndAddNewTags(projectInstance, tags):
    for tag_name in tags:
        lowered = str(tag_name).lower()
        searchtag = TagModel.objects.filter(tag_name=lowered)
        if len(searchtag) == 0:
            newtag = TagModel.objects.create(tag_name=lowered)
            newtag.save()
            projectInstance.tag.add(newtag)
        else:
            projectInstance.tag.add(searchtag[0])

class ProjectCreateMutation(graphene.Mutation):
    response = graphene.Boolean()
    message = graphene.String()
    projectInstance = graphene.Field(ProjectType)

    class Arguments:
        # logo = Upload(required=True, description="Logo for the Product.",)
        name = graphene.String(required=True)
        subtitle = graphene.String(required=True)
        description = graphene.String(required=True)
        tags = graphene.List(graphene.String, required=True)

    @classmethod
    def mutate(cls, root, info, name, subtitle, description, tags):
        try:
            with transaction.atomic():
                projectInstance = ProjectModel.objects.create(name=name, subtitle=subtitle, description=description, owner_id=info.context.user) 
                projectInstance.save()
                createAndAddNewTags(projectInstance, tags)
                return cls(projectInstance=projectInstance)
        except:
            return cls(message="Tranactional Error")

class MprsMutation(graphene.ObjectType):
    update_Comment = CommentUpdateMutation.Field()
    update_Reply = ReplyUpdateMutation.Field()
    update_Project = ProjectUpdateMutation.Field()
    delete_Comment = CommentDeleteMutation.Field()
    delete_Reply = ReplyDeleteMutation.Field()
    delete_Project = ProjectDeleteMutation.Field()
    delete_Screenshot = ScreenshotDeleteMutation.Field()
    create_Comment = CommentCreateMutation.Field()
    create_Reply = ReplyCreateMutation.Field()
    create_Project = ProjectCreateMutation.Field()
