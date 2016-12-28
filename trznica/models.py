from __future__ import unicode_literals

from django.db import models

class PonudbaStudenta(models.Model):
    studentId = models.CharField(max_length=10)
    studentSubject = models.CharField(max_length=100)
    studentOffer = models.CharField(max_length=100)
