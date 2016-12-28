from __future__ import unicode_literals

from django.db import models

class Ponudba(models.Model):
    student_id = models.CharField(max_length=10)
    student_offer = models.CharField(max_length=100)

class Offer(models.Model):
    student_id = models.CharField(max_length=10)
    subject = models.CharField(max_length=100)
    student_offer = models.CharField(max_length=100)
