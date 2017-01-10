from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    file = models.FileField(upload_to='documents')
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('User.CustomUser', null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey('classes.Predmet', null=True, on_delete=models.CASCADE)