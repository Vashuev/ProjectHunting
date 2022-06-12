from distutils.command.upload import upload
from email.policy import default

from core.utils import compressImage
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/',
                               default='avatars/default.jpg')

    def save(self, *args, **kwargs):
        self.avatar = compressImage(self.avatar)
        super(CustomUser, self).save(*args, **kwargs)
