# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext

from .models import *

def index(request):
	# user = User.objects.create_user(username="sh",email="shashankagarwal@gmail.com",password="shashank")
	# user.save()
	a = "shashnk"
	context_list={
		'a':a,
	}
	print "hello"
	return render_to_response('index.html',context_list,RequestContext(request) )

def signin(request):
	print "before"
	if request.POST:
		print "after"
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = User.objects.filter(email=email)
		print user
		# username = user.username
		if user is not None:
			user = authenticate(username = user[0].username,password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
					request.session['userid'] = user.id
					return HttpResponseRedirect('/dashboard/')
				else:
					return HttpResponseRedirect('/index/')
			else:
				return HttpResponseRedirect('/index/')
		else:
			return HttpResponseRedirect('/index/')

def signup(request):
	if request.POST:
		# username = request.POST.get('userame_signup')
		first_name = request.POST.get('first_name_signup')
		last_name = request.POST.get('last_name_signup')
		username = request.POST.get('username_signup')
		email = request.POST.get('email_signup')
		password = request.POST.get('password_signup')
		confirm_password = request.POST.get('confirm_password_signup')
		# print username,email,password
		us = username
		username=email                 #### We are taking username same as email
		if password == confirm_password:
			user = User.objects.create_user(username=username,email=email,password=password)
			user.first_name = first_name
			user.last_name = last_name
			user.username = us
			user.email = email
			request.session['userid'] = user.id
			user.save()
			user.is_active = True
			return HttpResponseRedirect('/dashboard/')
		else:
			return HttpResponse('Passwords do not match')

## This function is fired when update profile page is loaded 
def profile(request):
	### how to do deal with image is left
	userid = request.session['userid']
	user = User.objects.filter(id=request.session['userid'])
	user  = user[0]
	first_name = user.first_name
	last_name = user.last_name
	email = user.email
	username = user.username
	context_list = {
		'first_name' : first_name,
		'last_name' : last_name,
		'email': email,
		'username': username,
	}
	return render_to_response('profile.html',context_list,RequestContext(request))

## This function is fired when save changes are done on profile page
def update_profile(request):
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	email = request.POST.get('email')
	username = request.POST.get('username')
	password = request.POST.get('password')
	confirm_password = request.POST.get('confirm_password')
	userid = request.session['userid']
	user = User.objects.get(id=request.session['userid'])
	print user
	print "I am in google HQ"
	print user
	if password == confirm_password:
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.username = username
		user.set_password(password)
		print user
		user.save()
		return HttpResponseRedirect('/dashboard/')
	else:
		HttpResponse("Passwords do not match")

def dashboard(request):
	# user = request.user
	userid = request.session['userid']
	user = User.objects.filter(id=request.session['userid'])
	# user = User.objects.filter(username=user)
	print user[0]
	hotels = Hotel.objects.order_by('rating')
	restaurants = Restaurant.objects.order_by('rating')

	hotel_list = []
	restaurant_list = []
	# print hotels[0].image,restaurants[0].image

	for hotel in hotels:
		# img = hotel.image
		# img = str(img)
		# img1 = img.split('_')
		# temp = img1[0]
		# img = temp[1:]
		# if len(img1) != 1:
		# 	img = img + '.jpg'
		# print img
		# hotel.image = img
		print hotel.image.url
		hotel_list.append(hotel)

	for restaurant in restaurants:
		# img = restaurant.image
		# img = str(img)
		# img1 = img.split('_')
		# img = img1[0]
		# img = img[1:]
		# if len(img1) != 1:
		# 	img = img + '.jpg' 
		# print img
		# restaurant.image = img
		print restaurant.image.url
		restaurant_list.append(restaurant)

		rest_one = []
		rest_two = []
		hotel_one = []
		hotel_two = []
		
		rest_one = restaurant_list[:3]
		rest_two = restaurant_list[4:]
		hotel_one = hotel_list[:3]
		hotel_two = hotel_list[4:]

	context_list = {
		'rest_one': rest_one,
		'rest_two': rest_two,
		'hotel_one': hotel_one,
		'hotel_two': hotel_two,
		'user':user[0],
		'hotels': hotels,
		'restaurants': restaurants, 
	}
	return render_to_response('dashboard.html',context_list,RequestContext(request))

def search(request):
	search_query = request.POST.get('search')
	if search_query == "chilly food":
		restaurant = Restaurant.objects.order_by('rating')

		item_list = []
		for restaurant in restaurant:
			img = restaurant.image
			img = str(img)
			img1 = img.split('_')
			img = img1[0]
			img = img[1:]
			if len(img1) != 1:
				img = img + '.jpg' 
			print img
			restaurant.image = img
			restaurant_list.append(restaurant)
			name = str(restaurant.name)
			name = name.lower()
			if search_query.lower() in name:
				item_list.append(restaurant)
			
		for hotel in hotel.objects.order_by('rating'):
			name = str(hotel.name)
			name = name.lower()
			if search_query.lower() in name:
				item_list.append(hotel)


		context_list = {
			'restaurant':item_list[3:5],
		}
	return render_to_response('search.html',context_list,RequestContext(request))

def logout_user(request):
    del request.session['userid']
    logout(request)
    context_instance = RequestContext(request)
    return HttpResponseRedirect('/index/')
 
