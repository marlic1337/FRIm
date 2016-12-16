from django.conf.urls import url
from . import views

app_name = 'classes'

urlpatterns = [
    # /classes/
    url(r'^$', views.index, name='index'),
]