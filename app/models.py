from django.db import models
from pymongo import MongoClient
client = MongoClient("mongodb://hschipper:hannah1@104.198.148.208/congress")

# Create your models here.
class Bills(models.Model):
    billTitle = models.CharField(max_length=500)
    billHeading = models.CharField(max_length=100)
    billText = models.CharField(max_length=50000)
    committees = models.CharField(max_length=140)
    latestAction = models.CharField(max_length=200)
    sponser = models.CharField(max_length=200)
    status = models.CharField(max_length=140)
    def __str__(self):
        return self.title

class Members(models.Model):
    district = models.CharField(max_length=4)
    member = models.CharField(max_length=120)
    party = models.CharField(max_length=50)
    served = models.CharField(max_length=120)
    state = models.CharField(max_length=100)
    def __str__(self):
        return self.member

