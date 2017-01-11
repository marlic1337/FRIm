from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from string import join
from django.utils import timezone


from User.models import CustomUser as MyUser
from classes.models import Predmet

from datetime import datetime
import time


#Konverzija casa
def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset



# Create your models here.


class Forum(models.Model):
    title = models.CharField(max_length=100)
    predmet_id = models.ForeignKey(Predmet,blank=True,null=True,unique=True)


    def __unicode__(self):
        return self.title

    def num_posts(self):
        return sum([t.num_posts() for t in self.thread_set.all()])

    def last_post(self):
        if self.thread_set.count():
            last=None
            for t in self.thread_set.all():
                l = t.last_post()
                if l:
                    if not last: last = l
                    elif l.time > last.time: last=l
            return last



class Thread(models.Model):
    title = models.CharField(max_length=60)
    time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(MyUser,blank=True,null=True)
    forum = models.ForeignKey(Forum)

    def __unicode__(self):
        return u"%s - %s  " % (self.created_by, self.title)


    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return self.post_set.count() - 1

    def last_post(self):
        if self.post_set.count():
            return  self.post_set.order_by("-time")[0]




class Post(models.Model):
    title = models.CharField(max_length = 60)
    time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(MyUser, blank = True, null = True)
    thread = models.ForeignKey(Thread)
    body = models.TextField(max_length = 10000)

    def __unicode__(self):
        return u"%s - %s - %s " % (self.created_by, self.thread, self.title)

    def short(self):
        return u"V temi: %s \n %s %s \n %s " % (self.thread.title, self.created_by.first_name,self.created_by.last_name, datetime_from_utc_to_local(self.time).strftime("%Y-%m-%d %H:%M"))

    short.allow_tags = True
    def slika(self):
        s = self.created_by.logo_url()
        return s

class Subscriptions(models.Model):
    user = models.ForeignKey(MyUser)
    forum = models.ForeignKey(Forum)
