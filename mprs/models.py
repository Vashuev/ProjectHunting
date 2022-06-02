from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from datetime import datetime  

class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class TagModel(models.Model):
    tag_name = NameField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.tag_name


class ProjectModel(models.Model):
    logo = models.ImageField(upload_to='logos')
    name = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=500)
    posted_at = models.DateTimeField(auto_now_add=True)
    owner_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    upvote = models.PositiveIntegerField(default=0)
    tag = models.ManyToManyField(TagModel, related_name="projects")

    def __str__(self) -> str:
        return self.name


class ScreenshotModel(models.Model):
    image = models.ImageField(upload_to='screenshots')
    project_id = models.ForeignKey(ProjectModel,related_name="screenshots", on_delete=models.CASCADE)


class CommentModel(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)
    project_id = models.ForeignKey(ProjectModel, related_name="comments", on_delete=models.CASCADE)
    owner_id = models.ForeignKey(get_user_model(), related_name="user_comments", on_delete=models.SET_DEFAULT, default=1)


class ReplyModel(models.Model):
    reply = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True)
    comment_id = models.ForeignKey(CommentModel,related_name="replies", on_delete=models.CASCADE)
    owner_id = models.ForeignKey(get_user_model(), related_name="user_replies", on_delete=models.SET_DEFAULT, default=1)

    
