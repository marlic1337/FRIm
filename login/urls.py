from django.conf.urls import url

from . import views

app_name = "login"
urlpatterns = [
    url(r'^$', views.login, name='login'),
    #url(r'^register/$', views.register, name='register'),
    #url(r'^(?P<user_id>[0-9]+)/$', views.detail, name='detail'),
]