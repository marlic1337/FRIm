from __future__ import unicode_literals

from django.db import models
from login.models import User

class PonudbaStudenta(models.Model):
    user = models.ForeignKey(User, default="1", on_delete=models.CASCADE)
    studentSubject = models.CharField(max_length=100)
    studentOffer = models.CharField(max_length=100)
    studentWish = models.CharField(max_length=100)
