from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson.json_util import dumps,loads
from bson import BSON
from bson import json_util
from .models import *
import pymongo
import json

client = pymongo.MongoClient("mongodb://hschipper:password@104.198.148.208/congress")
db = client.congress

# Create your views here.
def index(request):
    #return HttpResponse("Hello World")
    #bills = Bills.objects.all()
    context = {
        'title':"Home",
        'members':db.members.find({ 'state': "California"}),
        'bills': db.bills.find({ 'committees': "House - Natural Resources"}),
    }
    return render(request,'home.html',context)

@csrf_exempt
def bills(request):
    bills = db.bills.find({'committees':"House - Natural Resources"})
    bill = {}
    bill['bills']= dumps(bills)
    return JsonResponse(bill)

def members(request):
    members = db.members.find({'state':"California"})
    member = {}
    member['members']=dumps(members)
    return JsonResponse(member)
