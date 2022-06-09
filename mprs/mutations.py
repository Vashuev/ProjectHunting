from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from .models import TagModel, CommentModel, ProjectModel, ScreenshotModel, ReplyModel
from .graphenetype import UserType, TagType, CommentType, ProjectType, ScreenshotType, ReplyType
from graphene_file_upload.scalars import Upload
from django.db import DatabaseError, transaction
from .decorators import login_required
from core.settings import MEDIA_URL, BASE_DIR
import os

class UpvoteProject(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        shouldRemoveVote = graphene.Boolean()

    projectInstance = graphene.Field(ProjectType)
    error = graphene.Boolean()
    votedByMe = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, id, shouldRemoveVote):
        try:
            projectInstance = ProjectModel.objects.get(pk=id)
            all_voters = projectInstance.votedBy.all()
            curr_voter = get_user_model().objects.get(pk=info.context.user.id)
            if not shouldRemoveVote and curr_voter not in all_voters:
                projectInstance.votedBy.add(curr_voter)
                projectInstance.voteCount += 1
                projectInstance.save()
            elif shouldRemoveVote and curr_voter in all_voters:
                projectInstance.votedBy.remove(curr_voter)
                projectInstance.voteCount -= 1
                projectInstance.save()

            return cls(projectInstance=projectInstance, votedByMe=not shouldRemoveVote, message="", error = False)
        except:
            cls(message="<Project object > with id:{id} is not in database".format(id=id), error = True)

class CommentUpdateMutation(graphene.Mutation):
    message = graphene.String()
    error = graphene.Boolean()
    class Arguments:
        # The input arguments for this mutation
        comment = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    commentInstance = graphene.Field(CommentType)
    
    @classmethod
    @login_required
    def mutate(cls, root, info, comment, id):
        try:
            commentInstance = CommentModel.objects.get(pk=id)
            if commentInstance.owner_id != info.context.user:
                return cls(error=True, message = "You are not the owner of this comment")
            commentInstance.comment = comment
            commentInstance.save()
            return CommentUpdateMutation(commentInstance=commentInstance, error=False)
        except CommentModel.DoesNotExist:
            return cls(error=True, message = "<Comment object > with id:{id} is not in database".format(id=id))

class ReplyUpdateMutation(graphene.Mutation):
    error = graphene.Boolean()
    message = graphene.String()
    class Arguments:
        # The input arguments for this mutation
        reply = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    replyInstance = graphene.Field(ReplyType)

    @classmethod
    @login_required
    def mutate(cls, root, info, reply, id):
        try:
            replyInstance = ReplyModel.objects.get(pk=id)
            if replyInstance.owner_id != info.context.user:
                return cls(error=True, message = "You are not the owner of this reply")
            replyInstance.reply = reply
            replyInstance.save()
            return ReplyUpdateMutation(replyInstance=replyInstance, error=False)
        except ReplyModel.DoesNotExist:
            return cls(error=True, message = "<Reply object > with id:{id} is not in database".format(id=id))

def updateProjectTags(projectInstance, tags):
    assignedTags = projectInstance.tag.all()
    seta = set()
    setb = set()

    for tag in assignedTags:
        seta.add(tag.tag_name)
    for tag in tags:
        setb.add(tag.lower())

    tag_to_remove = seta.difference(setb)
    tag_to_add = setb.difference(seta)
    print(tag_to_remove)
    print(tag_to_add)

    for tag_name in tag_to_remove:
        searchtag = TagModel.objects.filter(tag_name=tag_name)
        if len(searchtag) > 0:
            projectInstance.tag.remove(searchtag[0])
    
    for tag_name in tag_to_add:
        searchtag = TagModel.objects.filter(tag_name=tag_name)
        if len(searchtag) == 0:
            newtag = TagModel.objects.create(tag_name=tag_name)
            newtag.save()
            projectInstance.tag.add(newtag)
        else:
            projectInstance.tag.add(searchtag[0])
        
        if len(projectInstance.tag.all()) >= 5:
            break

def updateScreenshot(projectInstance, screenshots):
    for screenshot in screenshots:
        instance = ScreenshotModel.objects.create(image=screenshot, project_id=projectInstance)
        instance.save()

def removeScreenshot(deleteScreenshot):
    for screenshot_name in deleteScreenshot:
        file_name = 'screenshots/' + screenshot_name.split('/')[-1]
        full_path = str(BASE_DIR) + str(MEDIA_URL) +  file_name
        os.remove(full_path)
        instance = ScreenshotModel.objects.filter(image = file_name)
        if len(instance):
            instance[0].delete()
        
    

class ProjectUpdateMutation(graphene.Mutation):
    error = graphene.Boolean()
    message = graphene.String()
    screenshotInstances = graphene.List(ScreenshotType)

    class Arguments:
        id = graphene.ID(required=True)
        logos = graphene.List(Upload)
        name = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()
        tags = graphene.List(graphene.String, required=True)
        screenshots = graphene.List(Upload)
        deleteScreenshot = graphene.List(graphene.String)

    projectInstance = graphene.Field(ProjectType)
    @classmethod
    @login_required
    def mutate(cls, root, info, id, logos, tags,screenshots,deleteScreenshot, name=None, subtitle=None, description=None):
        try:
            with transaction.atomic():
                projectInstance = ProjectModel.objects.get(pk=id)
                last_path = str(BASE_DIR) + str(MEDIA_URL) + str(projectInstance.logo)
                print("last logo :", projectInstance.logo)
                print(last_path)
                if projectInstance.owner_id != info.context.user:
                    return cls(error=True, message = "You are not the owner of this Project")
                if len(logos):
                    os.remove(last_path)
                    projectInstance.logo = logos[0]
                if name!= None:
                    projectInstance.name = name
                if subtitle != None:
                    projectInstance.subtitle = subtitle
                if description != None:
                    projectInstance.description = description
                projectInstance.save()
                updateProjectTags(projectInstance, tags)
                removeScreenshot(deleteScreenshot)
                updateScreenshot(projectInstance, screenshots)
                screenshotInstances = ScreenshotModel.objects.filter(project_id=projectInstance)
                return cls(projectInstance=projectInstance,screenshotInstances=screenshotInstances, error=False)
        except ProjectModel.DoesNotExist:
            return cls(error=True, message = "<Project object > with id:{id} is not in database".format(id=id))
        except:
            return cls(message="Tranactional Error", error=True)

class CommentDeleteMutation(graphene.Mutation):
    error = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        try:
            comment = CommentModel.objects.get(pk=id)
            if comment.owner_id != info.context.user:
                return cls(error=True, message = "You are not the owner of this comment")
            comment.delete()
            return cls(error=False, message="Comment Deleted")
        except CommentModel.DoesNotExist:
            return cls(error=True, message = "<Comment object > with id:{id} is not in database".format(id=id))

class ReplyDeleteMutation(graphene.Mutation):
    error = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        try:
            reply = ReplyModel.objects.get(pk=id)
            if reply.owner_id != info.context.user:
                return cls(error=True, message = "You are not the owner of this reply")
            reply.delete()
            return cls(error=False, message="reply Deleted")
        except ReplyModel.DoesNotExist:
            return cls(error=True, message = "<Reply object > with id:{id} is not in database".format(id=id))

class ProjectDeleteMutation(graphene.Mutation):
    error = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        try:
            project = ProjectModel.objects.get(pk=id)
            if project.owner_id != info.context.user:
                return cls(error=True, message = "You are not the owner of this Project")
            project.delete()
            return cls(error=False, message="Project Deleted")
        except ProjectModel.DoesNotExist:
            return cls(error=True, message = "<Project object > with id:{id} is not in database".format(id=id))

class CommentCreateMutation(graphene.Mutation):
    error = graphene.Boolean()
    message = graphene.String()
    commentInstance = graphene.Field(CommentType)

    class Arguments:
        id = graphene.ID()      # product id
        comment = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, id, comment):
        try:
            project = ProjectModel.objects.get(pk=id)
            commentInstance = CommentModel.objects.create(comment=comment, project_id = project, owner_id = info.context.user)
            commentInstance.save()
            return cls(commentInstance=commentInstance, error=False)
        except ProjectModel.DoesNotExist:
            return cls(error=True, message = "<Project object > with id:{id} is not in database".format(id=id))

class ReplyCreateMutation(graphene.Mutation):
    error = graphene.Boolean()
    message = graphene.String()
    replyInstance = graphene.Field(ReplyType)

    class Arguments:
        id = graphene.ID()      # comment id
        reply = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, id, reply):
        try:
            comment = CommentModel.objects.get(pk=id)
            replyInstance = ReplyModel.objects.create(reply=reply,comment_id=comment, owner_id = info.context.user)
            replyInstance.save()
            return cls(replyInstance=replyInstance, error=False)
        except CommentModel.DoesNotExist:
            return cls(error=True, message = "<Comment object > with id:{id} is not in database".format(id=id))


def createAndAddTags(projectInstance, tags):
    for tag_name in tags:
        lowered = str(tag_name).lower()
        searchtag = TagModel.objects.filter(tag_name=lowered)
        if len(searchtag) == 0:
            newtag = TagModel.objects.create(tag_name=lowered)
            newtag.save()
            projectInstance.tag.add(newtag)
        else:
            projectInstance.tag.add(searchtag[0])

        if len(projectInstance.tag.all()) >= 5:
            break

def createAndAddScreenshot(projectInstance, screenshots):
    for screenshot in screenshots:
        instance = ScreenshotModel.objects.create(image=screenshot, project_id=projectInstance)
        instance.save()

class ProjectCreateMutation(graphene.Mutation):
    error = graphene.Boolean()
    message = graphene.String()
    projectInstance = graphene.Field(ProjectType)
    screenshotInstances = graphene.List(ScreenshotType)

    class Arguments:
        logos = graphene.List(Upload)
        name = graphene.String(required=True)
        subtitle = graphene.String(required=True)
        description = graphene.String(required=True)
        tags = graphene.List(graphene.String, required=True)
        screenshots = graphene.List(Upload)

    @classmethod
    @login_required
    def mutate(cls, root, info, logos, name, subtitle, description, tags, screenshots):
        try:
            with transaction.atomic():
                projectInstance = ProjectModel.objects.create(logo=logos[0],name=name, subtitle=subtitle, description=description, owner_id=info.context.user) 
                projectInstance.save()
                print("created Project")
                createAndAddTags(projectInstance, tags)
                print('added tags')
                createAndAddScreenshot(projectInstance, screenshots)
                print("added screenshots")
                screenshotInstances = ScreenshotModel.objects.filter(project_id=projectInstance)
                return cls(projectInstance=projectInstance, screenshotInstances=screenshotInstances , error=False)
        except:
            return cls(message="Tranactional Error", error=True)

class MprsMutation(graphene.ObjectType):
    update_Comment = CommentUpdateMutation.Field()
    update_Reply = ReplyUpdateMutation.Field()
    update_Project = ProjectUpdateMutation.Field()
    delete_Comment = CommentDeleteMutation.Field()
    delete_Reply = ReplyDeleteMutation.Field()
    delete_Project = ProjectDeleteMutation.Field()
    create_Comment = CommentCreateMutation.Field()
    create_Reply = ReplyCreateMutation.Field()
    create_Project = ProjectCreateMutation.Field()
    upvote_Project = UpvoteProject.Field()
