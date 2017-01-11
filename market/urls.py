from django.conf.urls import url
from . import views

app_name = 'market'

urlpatterns = [
    # /classes/
    url(r'^$', views.index, name='index'),
    url(r'^makeoffer/$', views.makeoffer, name='makeoffer',),
    #url(r'^offers/$', views.offer, name='offer'),
    url(r'^makeoffer/(?P<subjectId>[0-9a-zA-Z]+)/$', views.createoffer, name='createoffer',),
    url(r'^myoffers/$', views.myoffers, name='myoffers'),
    url(r'^myoffers/deleteoffer/$', views.deleteOffer, name='deleteOffer'),
    url(r'^offercreated/$', views.migrateOffer, name='migrateOffer'),
    url(r'^alloffers/$', views.alloffers, name='alloffers'),
    url(r'^alloffers/offeraccepted/$', views.offeraccepted, name='offeraccepted'),
    url(r'^makeoffer/(?P<subjectId>[0-9a-zA-Z]+)/nochoice/', views.migrateOffer, name='migrateOffer'),
    url(r'^timetable/$', views.timetable, name='timetable'),
    url(r'^makeoffer/oneoffer/', views.oneoffer, name='oneoffer'),
]