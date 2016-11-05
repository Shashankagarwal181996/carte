# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext

from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *

import datetime

# @ensure_csrf_cookie
def index(request):
	a = "shashnk"
	context_list={
		'a':a,
	}
	print "hello"
	return render(request,'index.html',context_list)

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

def register(request):
	context_list = {}
	return render(request,'signup.html',context_list)

def signup(request):
	if request.POST:
		# username = request.POST.get('userame_signup')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
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
	user_profile = Profile.objects.filter(user=user)
	user_profile = user_profile[0]
	image = user_profile.image
	# img = user_profile.image
	# img = str(img)
	# img1 = img.split('_')
	# img = img1[0]
	# img = img[1:]
	# if len(img1) != 1:
	# 	img = img + '.jpg' 
	# print img[1:]
	# user_profile.image = img[1:]
	# print user_profile.image
	# image = img[1:]
	print image
	

	context_list = {
		'first_name' : first_name,
		'last_name' : last_name,
		'email': email,
		'username': username,
		'image' : image,
	}
	return render(request,'myaccount.html',context_list)

## This function is fired when save changes are done on profile page
def update_profile(request):
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	email = request.POST.get('email')
	username = request.POST.get('username')
	password = request.POST.get('password')
	confirm_password = request.POST.get('confirm_password')
	image = request.FILES.get('profile_picture')
	print image
	print username
	userid = request.session['userid']
	user = User.objects.get(id=request.session['userid'])

	if password == confirm_password:
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.username = username
		print username
		user.set_password(password)
		# user.image = image
		user.save()
		user_profile = Profile.objects.filter(user=user)
		if len(user_profile) == 0:
			user_profile = Profile.objects.create(user=user,image=image)
		else:
			user_profile[0].image = image
			user_profile = user_profile[0]
		# print user_profile.image
		img = user_profile.image
		img = str(img)
		img1 = img.split('_')
		img = img1[0]
		print img
		# img = img[1:]
		if len(img1) != 1:
			img = img + '.jpg' 
		# user_profile.image = img[1:]
		print user_profile.image
		user_profile.save()
		return HttpResponseRedirect('/dashboard/')
	else:
		HttpResponse("Passwords do not match")

def dashboard(request):
	userid = request.session['userid']
	user = User.objects.filter(id=request.session['userid'])
	print user[0]
	hotels = Hotel.objects.order_by('rating')
	restaurants = Restaurant.objects.order_by('rating')
	hotel_list = []
	restaurant_list = []

	for restaurant in restaurants:
		url = restaurant.name
		url = str(restaurant.name)
		restaurant.url = url.replace(" ","")
		img = restaurant.image
		img = str(img)
		img1 = img.split('_')
		img = img1[0]
		img = img[1:]
		if len(img1) != 1:
			img = img + '.jpg' 
		restaurant.image = img[1:]
		restaurant_list.append(restaurant)

	for hotel in hotels:
		url = hotel.name
		url = str(hotel.name)
		hotel.url = url.replace(" ","")
		img = hotel.image
		img = str(img)
		img1 = img.split('_')
		img = img1[0]
		img = img[1:]
		if len(img1) != 1:
			img = img + '.jpg' 
		hotel.image = img[1:]
		hotel_list.append(hotel)

		rest_one = []
		rest_two = []
		rest_three = []
		hotel_one = []
		hotel_two = []
		
		rest_one = restaurant_list[:4]
		rest_two = restaurant_list[4:8]
		rest_three = restaurant_list[8:12]
		hotel_one = hotel_list[:4]

	context_list = {
		'rest_one': rest_one,
		'rest_two': rest_two,
		'rest_three':rest_three,
		'hotel_one': hotel_one,
		'user':user[0],
		'restaurants': restaurants, 
	}
	return render(request,'dashboard.html',context_list)

def product_detail(request,name):
	name = name
	flag=0
	boolean = True
	related_places = []
	restaurant_list = []
	tags_places = []
	restaurants = Restaurant.objects.order_by('rating')
	print name
	restaurant_cuisine = []
	for restaurant in restaurants:
		tags_all = []
		names = str(restaurant.name)
		names = names.replace(" ","")
		restaurant_list.append(restaurant)

		if name in names:
			flag=1
			# img = restaurant.image
			# img = str(img)
			# img1 = img.split('_')
			# img = img1[0]
			# img = img[1:]
			# if len(img1) != 1:
			# 	img = img + '.jpg' 
			# restaurant.image = img[1:]
			place = restaurant
			restaurant.url = names
			flag=1
			category = "CUISINES"
			cuisines = restaurant.cuisines
			restaurant_cuisine = cuisines.split(',')
			for x in restaurant_cuisine:
				tags_places.append(x)
				x = str(x)
				x = x.lstrip()
		else:
			cuisines = str(restaurant.cuisines)
			tags_all = cuisines.split(',')
			for x in tags_all:
				x = str(x)
				x = x.lstrip()

		for x in tags_all:
			x = str(x)
			x = x.lstrip()
			if x in restaurant_cuisine:
				restaurant.url = names
				related_places.append(restaurant)
				break

	# print "related places"
	print related_places
	tags = []
	hotel_features = []
	if flag == 0:
		hotels = Hotel.objects.order_by('rating')
		for hotel in hotels:
			names = str(hotel.name)
			names = names.replace(" ","")			
			hotel.url = names
			place = hotel
			if name in names:
				flag=2
				category = "HOTEL FEATURES"
				hotel_features = str(hotel.hotel_tags)
				tags = hotel_features.split(',')
				tags_places = tags
				for x in tags:
					x = str(x)
					x = x.lstrip()
			else:
				features = str(hotel.hotel_tags)
				tags_all = features.split(',')
				for x in tags_all:
					x = str(x)
					x = x.lstrip()
			for x in tags_all:
				if x in tags:
					hotel.url = names
					related_places.append(hotel)
					break
				
	detail = Rate_Review.objects.all()
	rate_review_object = []
	for rate_review in detail:
		names = str(rate_review.item_name)
		names= names.replace(" ","")
		if names in name:
			rate_review_object.append(rate_review)
	
	date = datetime.date.today()
	# for restaurant in restaurants:
	# 	related_places.append(restaurant)
	print tags_places
	if rate_review_object:
		context_list={
			'place' : place,
			'category' : category,
			'tags':tags_places,
			'related_places': related_places[:3],
			'rate_review':rate_review_object,
			'date':date,
		}
	else:
		context_list={
			'place' : place,
			'tags':tags_places,
			'category' : category,
			'related_places': related_places[:3],
			'date':date,
			# 'rate_review':rate_review_object,
		}
	return render(request,'product_detail.html',context_list)

def add_review(request):
	review = request.POST.get('add_review')
	rating = request.POST.get('add_rating')
	name = request.POST.get('product_name')
	# rating = request.POST.get('add_rating')
	place = Restaurant.objects.filter(name=name)
	if not place:
		place = Hotel.objects.filter(name=name)
	userid = request.session['userid']
	users = User.objects.filter(id=request.session['userid'])
	new_review = Rate_Review.objects.create(review=review,rating=rating,item_name=name)
	new_review.save()
	
	new_review.user = users
	user_profile = Profile.objects.filter(user=users)
	user_profile = user_profile[0]
	new_review.user_profile = user_profile
	new_review.save()

	print place,new_review.review,name
	rate_review = Rate_Review.objects.filter(item_name=name)
	img = place[0].image
	img = str(img)
	img1 = img.split('_')
	img = img1[0]
	img = img[1:]
	if len(img1) != 1:
		img = img + '.jpg' 
		# print img
		place[0].image = img[1:]
	print place[0].image
	tags = []
	tags = str(place[0].cuisines).split(',')
	context_list = {
		'place':place[0],
		'rate_review':rate_review,
		'tags':tags,
	}
	return render(request,'review.html',context_list)


def search(request):
	search_query = request.GET.get('search')
	restaurant_list = Restaurant.objects.order_by('rating')
	hotel_list = Hotel.objects.order_by('rating')
	search_query = str(search_query)
	search_query = search_query.lower()
	print search_query
	item_list = []
	flag=0
	for restaurant in restaurant_list:
		name = restaurant.name
		name = str(name)
		url = restaurant.name
		url = str(restaurant.name)
		restaurant.url = url.replace(" ","")
		restaurant.save()
		description = restaurant.description
		cuisine = restaurant.cuisines
		cuisine = str(cuisine)
		cuisine = cuisine.split(',')

		img = restaurant.image
		img = str(img)
		img1 = img.split('_')
		img = img1[0]
		img = img[2:]
		if len(img1) != 1:
			img = img + '.jpg' 
		print img
		restaurant.image = img
		name = name.lstrip()
		if search_query in name.lower():
			item_list.append(restaurant)
			flag = 1
		if search_query in description.lower():
			item_list.append(restaurant)
			flag = 1
		if search_query in restaurant.city.lower():
			item_list.append(restaurant)
			flag=1
		for cuisine in cuisine:
			cuisine = cuisine.lstrip()
			print cuisine.lower()
			if search_query in cuisine.lower():
				item_list.append(restaurant)
				flag = 1
	if flag == 0:
		for hotel in hotel_list:
			name = hotel.name
			name = str(name)
			url = restaurant.name
			url = str(hotel.name)
			hotel.url = url.replace(" ","")
			hotel.save()
			description = hotel.description
			# description = str(description)
			hotel_tags = hotel.hotel_tags
			hotel_tags = str(hotel_tags)
			hotel_tags = hotel_tags.split(',')

			img = hotel.image
			img = str(img)
			img1 = img.split('_')
			img = img1[0]
			img = img[1:]
			if len(img1) != 1:
				img = img + '.jpg' 
			print img
			hotel.image = img

			if search_query in name.lower():
				item_list.append(hotel)
				flag = 2
			if search_query in description.lower():
				item_list.append(hotel)
				flag = 2
			if search_query in hotel.city.lower():
				item_list.append(hotel)
			for hotel_tags in hotel_tags:
				if search_query in hotel_tags.lower():
					item_list.append(hotel)
					flag = 2
	print item_list
	context_list = {
		'places':item_list,		
	}
	return render(request,'search.html',context_list)

def logout_user(request):
    del request.session['userid']
    logout(request)
    context_instance = RequestContext(request)
    return HttpResponseRedirect('/index/')
 
