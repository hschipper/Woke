from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'bills', views.bills, name='bills'),
    url(r'members', views.members, name='members'),
    url(r'member_page',views.member_page, name='member_page'),
    url(r'bill_page',views.bill_page, name='bill_page'),
    url(r'register',views.register,name='register'),
    url(r'committees',views.committees,name='committees'),
    url(r'text',views.text,name='text'),
    url(r'home',views.index, name='home'),
    url(r'profile',views.profile, name='profile'),
    url(r'hot',views.hot,name='hot'),
    url(r'bill_details', views.bill_details, name='bill_details'),
]
