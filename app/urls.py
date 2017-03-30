from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'bills', views.bills, name='bills'),
    url(r'members', views.members, name='members'),
    url(r'member_page',views.member_page, name='member_page'),
    url(r'array',views.array, name='array'),
    url(r'register',views.register,name='register'),
]
