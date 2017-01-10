from django.conf.urls import url

from . import views

app_name = "User"
urlpatterns = [
    url(r'^settings', views.changeUserSettings, name='changeUserSettings'),
]