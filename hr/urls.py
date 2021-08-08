from django.conf.urls import url
from . import views

urlpatterns = [
    url('^home$', views.index, name='index'),
    url('^$', views.home, name='home'),
    url('^process_url_from_client', views.process_url_from_client, name='process_url_from_client')
]