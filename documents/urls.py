from django.conf.urls import url

from . import views

app_name = 'documents'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<class_id>[0-9A-Z]+)$', views.list, name='list'),
    url(r'^(?P<class_id>[0-9A-Z]+)/upload/$', views.upload, name='upload'),
    url(r'^(?P<class_id>[0-9A-Z]+)/(?P<document_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<class_id>[0-9A-Z]+)/(?P<document_id>[0-9]+)/download/$', views.download, name='download'),
    url(r'^(?P<class_id>[0-9A-Z]+)/(?P<document_id>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<class_id>[0-9A-Z]+)/(?P<document_id>[0-9]+)/update/$', views.update, name='update'),
]