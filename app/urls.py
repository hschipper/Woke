from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'bills', views.bills, name='bills'),
    url(r'members', views.members, name='members'),
]
