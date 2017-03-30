from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from bson.json_util import dumps,loads
from bson import BSON
from bson import json_util
from .models import *
from .forms import *
from django.contrib.auth import authenticate
import pymongo
import json
#connect to database
client = pymongo.MongoClient("mongodb://hschipper:hannah1@104.198.148.208/congress")
db = client.congress

#main home page
def index(request):
    context = {
        'title':"Home",
        'members':db.members.find({ 'state': "California"}),
        'bills': db.bills.find({ 'committees': "House - Natural Resources"}),
        "member_page":"/member_page",
    }
    return render(request,'home.html',context)

#API for app
@csrf_exempt
def bills(request):
    bills = db.bills.find({'committees':"House - Natural Resources"})
    bill = {}
    bill['bills']= dumps(bills)
    return JsonResponse(bill)

#API for app
def members(request):
    members = db.members.find({'state':"Colorado",'district':"1"})
    member = {}
    member['members']=dumps(members)
    return HttpResponse(member['members'])

def array(request):
    cursor = db.members.find({'state':"California"})
    member = {}
    member['members']= []
  #  obj = next(cursor, None)
  #  if obj:
    for obj in cursor:
        member['members']+={
            'member':obj['member'],
            'state':obj['state'],
        }
    return JsonResponse(member)

def register(request):
    if request.method == "POST":
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'))
            return HttpResponseRedirect('/')
    else:
        form = registration_form()
    context = {
        'title':'Register',
        'form':form
    }
    return render(request, 'register.html', context)



#second page to display members different.
def member_page(request):
    context= {
        'title':"Members",
        'members':db.members.find({'member':"Representative LaMalfa, Doug"}),
        'bills':db.bills.find({'committees':"House - Natural Resources"}),
        'home':"/",
    }
    return render(request,'member_page.html',context)
