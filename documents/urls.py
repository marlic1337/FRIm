from django.conf.urls import url

from . import views

app_name = 'documents'
urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^(?P<document_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<document_id>[0-9]+)/download/$', views.download, name='download'),
    url(r'^(?P<document_id>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<document_id>[0-9]+)/update/$', views.update, name='update'),
]