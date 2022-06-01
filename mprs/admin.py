from django.contrib import admin
from .models import TagModel, CommentModel, ScreenshotModel, ProjectModel, ReplyModel

admin.site.register(TagModel)
admin.site.register(CommentModel)
admin.site.register(ScreenshotModel)
admin.site.register(ProjectModel)
admin.site.register(ReplyModel)
