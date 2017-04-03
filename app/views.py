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
    if request.method == 'POST':
        form = MemberSearch(request.POST)
        if form.is_valid():
#            zipcode = request.POST.get('search', None)
            search = form.cleaned_data['memberSearch']
#            zipcode = zipSearch(zipcode=search)
#            zipcode.save()
            form = MemberSearch()
        else:
            search = ""
    else:
        form = MemberSearch()
        search = "Texas"
    context = {
        'title':"Home",
        'members':db.members.find({ 'state': search}),
        'bills': db.bills.find({ 'committees': "House - Natural Resources"}),
        'form': form,
        'search':search,
        "member_page":"/member_page",
    }
    return render(request,'home.html',context)

#API for app
@csrf_exempt
def bills(request):
    bills = db.bills.find({'committees':"House - Natural Resources"})
    bill = {}
    bill['bills']= dumps(bills)
    return HttpResponse(bill['bills'])

#API for app
def members(request):
    members = db.members.find({'state':"Colorado"})
    member = {}
    member['members']=dumps(members)
    return HttpResponse(member['members'])

def bill_page(request):
    bills = db.bills.find({'committees':request.GET['committee']})
    bill = {}
    bill['bills']=dumps(bills)
    return HttpResponse(bill['bills'])

def committees(request):
    committees = db.committees.find({})
    committee = {}
    committee['committees']=dumps(committees)
    return HttpResponse(committee['committees'])

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
    members = db.members.find({'state':request.GET['state']})
    member = {}
    member['members']=dumps(members)
    return HttpResponse(member['members'])
