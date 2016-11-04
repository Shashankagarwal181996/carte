from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from datetime import *
from django.contrib.auth.models import User

from carte.choices import *

class Profile(models.Model):
	image = models.ImageField()
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,default=1)


class Rate_Review(models.Model):
	review = models.TextField()
	rating = models.FloatField()
	user = models.ManyToManyField(User,blank=True)
	item_name = models.CharField(max_length=100)

	def __str__(self):
		return self.review

class Restaurant(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100,null=True)
	location = models.CharField(max_length=200)
	city = models.CharField(max_length=100)
	rating = models.FloatField()
	# review = models.TextField()
	image = models.ImageField()
	rate_review = models.ManyToManyField(Rate_Review,blank=True)
	description = models.TextField()
	cuisines = models.TextField()
	url = models.TextField()

	def __str__(self):
		return self.name

class Hotel(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100,null=True)
	location = models.CharField(max_length=200)
	city = models.CharField(max_length=100)
	rating = models.FloatField()
	# review = models.TextField()
	image = models.ImageField()
	rate_review = models.ManyToManyField(Rate_Review,blank=True)
	description = models.TextField()
	hotel_tags = models.TextField()
	url = models.TextField()
	

	def __str__(self):
		return self.name

