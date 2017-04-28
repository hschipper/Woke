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
        committee = "House - Natural Resources"
        if form.is_valid():
            search = form.cleaned_data['memberSearch']
            form = MemberSearch()
        else:
            search = ""
    else:
        form = MemberSearch()
        if ('committee' in request.GET):
            committee = request.GET['committee'] 
        else:
            committee = "House - Natural Resources"
        if not request.user.is_authenticated():
            search = "Texas"
        else:
            profile = Profile.objects.get(user = request.user)
            if profile:
                search = profile.state
                committee = profile.committees

    context = {
        'title':"Home",
        'members':db.members.find({ 'state': search}),
        'bills': db.bills.find({ 'committees': committee}),
        'form': form,
        'search':search,
        "member_page":"/",
    }
    return render(request,'home.html',context)

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            committee = form.cleaned_data['committees']
            form = ProfileForm()
            user = request.user
            profile = Profile.objects.get(user = request.user)
            profile.update(state, committee)

    else:
        form = ProfileForm()
            
    context = {
        'title':"Settings",
        'form': form,
    }
    return render(request,'my_profile.html',context)

def text(request):
    text = db.bills.find({'billTitle':request.GET['title']},{'billText':1})
    context = {
        'title': "bill text",
        'billTitle':request.GET['title'],
        'billText':text[0]['billText'],
    }
    return render(request,'text.html',context)


#API for app
@csrf_exempt
def bills(request):
    if ('committee' in request.GET):
        committee = request.GET['committee']    
    else:
        committee = "House - Natural Resources"
    context = {
        'title': "bills",
        'bills': db.bills.find({ 'committees': committee }),
    }
    return render(request,'bills.html',context)

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
        form2 = ProfileForm(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form.save()
            profile = Profile.create(form2.cleaned_data['state'],form2.cleaned_data['committees'],user)
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'))
            profile.save()
            return HttpResponseRedirect('/')
    else:
        form = registration_form()
        form2 = ProfileForm()
    context = {
        'title':'Register',
        'form':form,
        'form2':form2
    }
    return render(request, 'register.html', context)



#second page to display members different.
def member_page(request):
    members = db.members.find({'state':request.GET['state']})
    member = {}
    member['members']=dumps(members)
    return HttpResponse(member['members'])
