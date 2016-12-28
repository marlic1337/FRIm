from django.conf.urls import url
from . import views

app_name = 'trznica'

urlpatterns = [
    # /classes/
    url(r'^$', views.index, name='index'),
    url(r'^makeoffer/$', views.makeoffer, name='makeoffer',),
    #url(r'^offers/$', views.offer, name='offer'),
    url(r'^makeoffer/(?P<subjectId>[0-9a-zA-Z]+)/$', views.createoffer, name='createoffer',),
    url(r'^myoffers/$', views.myoffers, name='myoffers'),
    url(r'^offercreated/$', views.migrateOffer, name='migrateOffer'),
]