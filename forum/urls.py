from django.conf.urls import url, include
from django.views.generic import ListView,DetailView
from forum.models import *

from . import views


urlpatterns = [

    url(r'^$', views.index,name='index'),
    url(r'^subforum/(?P<pk>\d+)/$', views.subforum,name='subforum'),
    url(r'^thread/(?P<pk>\d+)/$', views.thread,name='thread'),
    url(r'^post/(?P<ptype>new_thread|reply|edit)/(?P<id>\d+)/$', views.postForm, name='post'),
    url(r'reply/(?P<id>\d+)/$',views.reply, name='reply'),
    url(r'new_thread/(?P<id>\d+)/$', views.new_thread, name='new_thread'),
    url(r'edit/(?P<id>\d+)/$', views.edit, name='edit'),

]
