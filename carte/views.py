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
import math


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
			print user
			if user is not None:
				if user.is_active:
					login(request,user)
					request.session['userid'] = user.id
					return HttpResponseRedirect('/dashboard/')
				else:
					return HttpResponseRedirect('/index/')
			else:
				# return HttpResponseRedirect('/index/')
				state = "Password is incorrect."
				print state
				context_list = {
					'state': state,
				}
				return render(request,'index.html',context_list)
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
			state = "Passwords do not match."
			print state
			context_list = {
				'state': state,
			}
			return render(request,'signup.html',context_list)

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
	if len(user_profile) != 0:
		user_profile = user_profile[0]
		image = user_profile.image
		print image

		context_list = {
			'first_name' : first_name,
			'last_name' : last_name,
			'email': email,
			'username': username,
			'image' : image,
		}
	else:
		context_list = {
			'first_name' : first_name,
			'last_name' : last_name,
			'email': email,
			'username': username,
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

	if password == "":
		
		print "empty"
		user_profile = Profile.objects.filter(user=user)
		print user_profile
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

	elif password == confirm_password:
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.username = username
		print username
		user.set_password(password)
		# user.image = image
		user.save()
		user_profile = Profile.objects.filter(user=user)
		print user_profile
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
		state = "Passwords do not match."
		print state
		user_profile = Profile.objects.filter(user=user)
		if len(user_profile) != 0:
			user_profile = user_profile[0]
			image = user_profile.image
			context_list = {
				'state': state,
				'first_name' : first_name,
				'last_name' : last_name,
				'email': email,
				'username': username,
				'image': image,
			}
		else:
			context_list = {
				'state': state,
				'first_name' : first_name,
				'last_name' : last_name,
				'email': email,
				'username': username,
			}
		return render(request,'myaccount.html',context_list)

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
		# img = img[1:]
		# print img
		if len(img1) != 1:
			img = img + '.jpg' 
		hotel.image = img
		print hotel.image
		hotel_list.append(hotel)

		rest_one = []
		rest_two = []
		rest_three = []
		hotel_one = []
		hotel_two = []
		
		restaurant_list.reverse()
		hotel_list.reverse()

		rest_one = restaurant_list[:4]
		rest_two = restaurant_list[4:8]
		rest_three = restaurant_list[8:12]
		hotel_one = hotel_list[:4]
		hotel_two = hotel_list[4:8]

	context_list = {
		'rest_one': rest_one,
		'rest_two': rest_two,
		'rest_three':rest_three,
		'hotel_one': hotel_one,
		'hotel_two': hotel_two,
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
	# print related_places
	tags = []
	hotel_features = []
	print "hotel"
	if flag == 0:
		hotels = Hotel.objects.order_by('rating')
		for hotel in hotels:
			names = str(hotel.name)
			names = names.replace(" ","")			
			
			if name in names:
				hotel.url = names
				place = hotel
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
	rate_review_object.reverse()
	date = datetime.date.today()
	# for restaurant in restaurants:
	# 	related_places.append(restaurant)
	# print tags_places

	# mat = []
	# user = User.objects.filter(id=request.session['userid'])
	# rate_review = Rate_Review.objects.filter(user=user)
	# rate_review_all = Rate_Review.objects.all()
	# print rate_review
	# count = 0
	# temp = []
	# temp.append("user")
	# restaurant = Restaurant.objects.all()
	# for restaurant in restaurant:
	# 	temp.append(restaurant.name)
	# mat.append(temp)
	# for rate_review in rate_review:
	# 	temp = []
	# 	temp.append()
	# 	temp.append(rate_review)

	temp= []
	counter = 0
	# x = User.objects.filter(username='hs')
	# rate_review = Rate_Review.objects.filter(user=x)
	# print rate_review[0].user
	# restaurants = Restaurant.objects.all()
	# for x in User.objects.all():
	# 	# print x.username
	# 	rate_review = Rate_Review.objects.filter(user=x)
	# 	if rate_review:
	# 		rate_review = rate_review[0]
	# 	# if len(rate_review)!=0 :
	# 		# print rate_review.rating
	# 		counter = counter+1
	# 		# for y in rate_review:
	# 		res = []
	# 		res.append(x)
	# 		res.append(rate_review.item_name)
	# 		res.append(rate_review.rating)
	# 		print res
	# 		temp.append(res)
	# print temp
		# if rate_review.item_name is not None:
		# 	counter = counter+1
		# 	for y in rate_review:
		# 		res = []
		# 		res.append(x)
		# 		res.append(rate_review.item_name)
		# 		res.append(rate_review.rating)
		# 		temp.append(res)
		# 	print temp
	# print("Collaborative Filtering")

	# mat = []
	# mat.append([4,-10,-10,5,1,-10,-10])
	# mat.append([5,5,4,-10,-10,-10,-10])
	# mat.append([-10,-10,-10,2,4,5,-10])
	# mat.append([-10,3,-10,-10,-10,-10,3])

	# #subtracting the average of each user from respective ratings
	# avgs=[]

	# for i in range(len(mat)):
	#     av = 0.0
	#     tot = 0
	#     for j in mat[i]:
	#         if j != -10:
	#             av = av + j
	#             tot += 1            
	#     av = av / tot
	#     avgs.append(av)
	#     for j in range(len(mat[i])):
	#         if mat[i][j] != -10:
	#             mat[i][j] = mat[i][j] - av


	# #all root of square sum
	# root_sqs=[]
	# for i in mat:
	#     sqs = 0
	#     for j in i:
	#         if j != -10:
	#             sqs = sqs + j*j
	#     root_sqs.append(math.sqrt(sqs))

	# #cosine relation of activ user with every other user
	# activ = 0
	# all_similr=[]

	# for i in range(len(mat)):
	#     val = 0
	#     if activ == i:
	#         continue
	#     for j in range(len(mat[i])):
	#         if mat[i][j] != -10 and mat[activ][j] != -10:
	#             val = val + mat[i][j]*mat[activ][j]

	#     if(root_sqs[i] != 0):       
	#         val = val / (root_sqs[activ]*root_sqs[i])
	#         all_similr.append([val, i])
	            
	# all_similr.sort()
	# all_similr.reverse() #now it has all relations in decending order
	# print(all_similr)

	# predic = avgs[activ]
	# item = 1
	# val = 0
	# tot = 0

	# for i in all_similr:
	#     usr = i[1]
	#     if mat[usr][item] != -10:
	#         val += mat[usr][item]*i[0]
	#         print(usr)
	#     tot += i[0]

	# predic += (val / tot)
	# print(predic)

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
	rating_count = request.POST.get('rating_count')
	rating = rating_count
	if rating is None:
		rating = 4
	print review,rating,name
	print rating
	# rating = request.POST.get('add_rating')
	place = Restaurant.objects.filter(name=name)
	flag=0
	if not place:
		place = Hotel.objects.filter(name=name)
		flag=1
	userid = request.session['userid']
	users = User.objects.filter(id=request.session['userid'])
	new_review = Rate_Review.objects.create(review=review,rating=rating,item_name=name)
	new_review.save()
	
	new_review.user = users
	user_profile = Profile.objects.filter(user=users)
	if user_profile:
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
	if flag==0:
		tags = str(place[0].cuisines).split(',')
	else:
		tags = str(place[0].hotel_tags).split(',')

	restaurants = Restaurant.objects.order_by('rating')
	print name
	restaurant_cuisine = []
	restaurant_list=[]
	related_places = []
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
	# print related_places
	tags = []
	hotel_features = []
	print "hotel"
	if flag == 0:
		hotels = Hotel.objects.order_by('rating')
		for hotel in hotels:
			names = str(hotel.name)
			names = names.replace(" ","")			
			
			if name in names:
				hotel.url = names
				place = hotel
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
	# rate_review.reverse()
	list(rate_review).reverse()
	print rate_review
	context_list = {
		'place':place[0],
		'rate_review':rate_review,
		'tags':tags,
		'related_places': related_places,
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
			print img
			img = str(img)
			img1 = img.split('_')
			img = img1[0]
			# img = img[1:]
			# print img
			if len(img1) != 1:
				img = img + '.jpg' 
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
	item_list = list(set(item_list))
	if len(item_list) == 0:
		context_list={}
		return render(request,'404.html',context_list)
	context_list = {
		'places':item_list,		
	}
	return render(request,'search.html',context_list)

def logout_user(request):
    del request.session['userid']
    logout(request)
    context_instance = RequestContext(request)
    return HttpResponseRedirect('/index/')
 
def contact_us(request):
	context_list={}
	return render(request,'contact.html',context_list)

def about_us(request):
	context_list = {}
	return render(request,'about.html',context_list)