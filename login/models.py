from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    displayName = models.CharField(max_length=20)
    mail = models.CharField(max_length=30)
    studentId = models.CharField(max_length=10)
