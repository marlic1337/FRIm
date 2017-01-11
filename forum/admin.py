from django.contrib import admin
from forum.models import *
# Register your models here.




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