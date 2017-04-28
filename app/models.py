from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from pymongo import MongoClient
client = MongoClient("mongodb://hschipper:hannah1@104.198.148.208/congress")

# Create your models here.
class Bills(models.Model):
    billTitle = models.CharField(max_length=500, default = "")
    billHeading = models.CharField(max_length=100, default = "")
    billText = models.CharField(max_length=50000, default = "")
    committees = models.CharField(max_length=140, default = "")
    latestAction = models.CharField(max_length=200, default = "")
    sponser = models.CharField(max_length=200, default = "")
    status = models.CharField(max_length=140, default = "")
    def __str__(self):
        return self.title

class Members(models.Model):
    district = models.CharField(max_length=4, default = "")
    member = models.CharField(max_length=120, default = "")
    party = models.CharField(max_length=50, default = "")
    served = models.CharField(max_length=120, default = "")
    state = models.CharField(max_length=100, default = "")
    def __str__(self):
        return self.member


class zipSearch(models.Model):
    zipcode = models.CharField(max_length=5)
    def __str__(self):
        return self.zipcode


#adding extra attributes to the user model
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    state = models.CharField(max_length=100)
    committees = models.CharField(max_length=200, default="")
    @classmethod
    def create(cls, s, c, user):
        profile = cls(state=s, committees=c)
        profile.user = user
        profile.save()
        return profile
    def update(cls, s, c):
        cls.state = s
        cls.committees = c
        cls.save()
        return cls

