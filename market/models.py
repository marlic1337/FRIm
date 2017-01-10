from __future__ import unicode_literals

from django.db import models
from User.models import CustomUser

class PonudbaStudenta(models.Model):
    user = models.ForeignKey(CustomUser, default="1", on_delete=models.CASCADE)
    studentSubject = models.CharField(max_length=100)
    studentOffer = models.CharField(max_length=100)
    studentWish = models.CharField(max_length=100)
    accepted = models.BooleanField(default=False)
    acceptedBy = models.CharField(max_length=100)
