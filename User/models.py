from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    studentId = models.CharField(max_length=10)

    REQUIRED_FIELDS = ['email', 'studentId']

    logo = models.ImageField(upload_to='profile_pic', width_field='logo_width', height_field='logo_height', null=True,
                             blank=True)
    logo_width = models.PositiveIntegerField(null=True)
    logo_height = models.PositiveIntegerField(null=True)

    def logo_url(self):
        if self.logo:
            return self.logo.url
        return settings.MEDIA_URL + 'profile_pic/default_user.png'

class SocialNetworks(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True)

    url_facebook = models.CharField(max_length=64, blank=True)
    url_googleplus = models.CharField(max_length=64, blank=True)
    url_twitter = models.CharField(max_length=64, blank=True)
    url_linkedin = models.CharField(max_length=64, blank=True)
    url_github = models.CharField(max_length=64, blank=True)