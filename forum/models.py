from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from string import join

from User.models import CustomUser as MyUser



# Create your models here.


class Forum(models.Model):
    title = models.CharField(max_length=30)

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
                    elif l.created > last.created: last=l
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
            return  self.post_set.order_by("time")[0]





class Post(models.Model):
    title = models.CharField(max_length = 60)
    time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(MyUser, blank = True, null = True)
    thread = models.ForeignKey(Thread)
    body = models.TextField(max_length = 10000)

    def __unicode__(self):
        return u"%s - %s - %s " % (self.created_by, self.thread, self.title)

    def short(self):
        return u"%s - %s\n %s " % (self.created_by, self.title, self.time.strftime("%b %d, %I:%M %p"))
    short.allow_tags = True


##Admin

class ForumAdmin(admin.ModelAdmin):
    pass


class ThreadAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "created_by", "time"]
    list_filter = ["forum","created_by"]

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "created_by"]
    list_display = ["title","thread", "created_by","time"]


admin.site.register(Forum,ForumAdmin)
admin.site.register(Thread,ThreadAdmin)
admin.site.register(Post,PostAdmin)