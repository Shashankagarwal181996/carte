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
	rest_four = []
	rest_five = []

	hotel_one = []
	hotel_two = []
	hotel_three = []
	
	restaurant_list.reverse()
	hotel_list.reverse()
	print restaurant_list
	rest_one = restaurant_list[:4]
	rest_two = restaurant_list[4:8]
	rest_three = restaurant_list[8:12]
	rest_four = restaurant_list[12:16]
	rest_five = restaurant_list[16:20]
	
	hotel_one = hotel_list[:4]
	hotel_two = hotel_list[4:8]
	hotel_three = hotel_list[8:12]
	hotel_four = hotel_list[12:16]


	# """ Code for recommendations on dashboard."""
	import math

	print("User-User based Collaborative Filtering")
	userid = request.session['userid']
	user = User.objects.filter(id=request.session['userid'])
	users = User.objects.all()
	# hotels = Hotel.objects.all()
	# restaurants = Restaurant.objects.all()
	# rate_review = Rate_Review.objects.all()
	# usrs = []
	# htls = []
	# rsts = []
	# rvws = []
	# for user in users:
	# 	usrs.append(str(user.username))
	# print usrs

	# for hotel in hotels:
	# 	htls.append(str(hotel.name))
	# print htls
	
	# for restaurant in restaurants:
	# 	rsts.append(str(restaurant.name))
	# print rsts
	
	# x = Rate_Review.user.all()
	# print x

	# for user in users:
	# 	temp = []
	# 	x = Rate_Review.objects.filter(user=user)
	# 	if len(x)!=0:
	# 		temp.append(str(user.username))
	# 		temp.append(str(x[0].item_name))
	# 		temp.append(x[0].rating)
	# 		print temp
	# 		rvws.append(temp)
	# print rvws
	# # usrs = ["hihi", "haha", "hahi", "hahu"]
	# # htls = ["titi","tata","lolo","nene"]
	# # rsts = ["titi1","tata1","lolo1","nene1"]
	# # rvws = [["hihi", "titi",4],
	# #         ["hihi", "lolo",4.5],
	# #         ["haha", "tata",2],
	# #         ["haha", "lolo",3],
	# #         ["hahi", "titi",4.5],
	# #         ["hahi", "nene",3.5],
	# #         ["hahu", "titi",1],
	# #         ["hahu", "tata",4.5],
	# #         ["hahu", "lolo",2],
	# #         ["hahu", "nene",2],
	# #         ["hihi", "titi1",4],
	# #         ["hihi", "lolo1",4.5],
	# #         ["haha", "tata1",2],
	# #         ["haha", "lolo1",3],
	# #         ["hahi", "titi1",4.5],
	# #         ["hahi", "nene1",3.5],
	# #         ["hahu", "titi1",1],
	# #         ["hahu", "tata1",4.5],
	# #         ["hahu", "lolo1",2],
	# #         ["hahu", "nene1",2]]
	# userid = request.session['userid']
	# user = User.objects.filter(id=request.session['userid'])

	# activ_usr = user[0].username #yaha dal de user ka naam
	# usrs_ind = {}
	# htls_ind = {}
	# rsts_ind = {}
	# for i in range(len(usrs)):
	#     usrs_ind[usrs[i]] = i
	# for i in range(len(htls)):
	#     htls_ind[htls[i]] = i
	# for i in range(len(rsts)):
	#     rsts_ind[rsts[i]] = i

	# activ = usrs_ind[activ_usr]

	# ##HOTEL_PART############

	# mat = [[-10]*len(htls) for _ in range(len(usrs))]

	# for i in rvws:
	#     if i[1] in htls:
	#         mat[usrs_ind[i[0]]][htls_ind[i[1]]] = i[2]
	# # print(mat)

	# #subtracting the average of each user from respective ratings

	# avgs=[]
	# for i in range(len(mat)):
	#     av = 0.0
	#     tot = 0
	#     for j in mat[i]:
	#         if j != -10:
	#             av = av + j
	#             tot += 1
	#     if(tot != 0):
	#         av = av / tot
	#         avgs.append(av)
	#         for j in range(len(mat[i])):
	#             if mat[i][j] != -10:
	#                 mat[i][j] = mat[i][j] - av


	# #all root of square sum
	# root_sqs=[]
	# for i in mat:
	#     sqs = 0
	#     for j in i:
	#         if j != -10:
	#             sqs = sqs + j*j
	#     root_sqs.append(math.sqrt(sqs))

	# #cosine relation of activ user with every other user
	# all_similr=[]
	# ans = []

	# for i in range(len(mat)):
	#     val = 0
	#     if activ == i:
	#         continue
	#     for j in range(len(mat[i])):
	#         if mat[i][j] != -10 and mat[activ][j] != -10:
	#             val = val + mat[i][j]*mat[activ][j]

	#     if(root_sqs[i] != 0 and val != 0 and root_sqs[activ] != 0):    
	#         val = val / (root_sqs[activ]*root_sqs[i])
	#         all_similr.append([val, i])

	# if len(all_similr) != 0:
	#     all_similr.sort()
	#     all_similr.reverse() #now it has all relations in decending order
	#     # print(all_similr)

	#     for j in range(len(mat[activ])):
	#         if mat[activ][j] != -10:#already there
	#             continue
	#         predic = avgs[activ]
	#         item = j
	#         tot = 0
	#         val = 0
	#         for i in all_similr:
	#             usr = i[1]
	#             if mat[usr][item] != -10:
	#                 val += mat[usr][item]*i[0]
	#                 #print(usr)
	#             tot += i[0]

	#         predic += (val / tot)
	#         if predic >= 2.1:
	#             ans.append(j)
	#             # print(predic)

	#     if len(ans) == 0:   #if no similar user rated this item then not possible or if users found but no item had sufficiently big predicted value
	#         ans.append(0)
	#         ans.append(1)
	#         ans.append(2)
	#         ans.append(3)
	        
	# else:       ##in case not possible if no similar users found
	#     ans.append(0)
	#     ans.append(1)
	#     ans.append(2)
	#     ans.append(3)
	    
	# print(ans)  ##here is final list of indexes############
	# final_lst=[]
	# for i in ans:
	#     final_lst.append(htls[i])
	# print(final_lst)

	# final_hotel_list = []
	# for hotel in final_lst:
	# 	a = Hotel.objects.filter(name=hotel)
	# 	final_hotel_list.append(a)

	# ##RESTR_PART############

	# mat = [[-10]*len(rsts) for _ in range(len(usrs))]

	# for i in rvws:
	#     if i[1] in rsts:
	#         mat[usrs_ind[i[0]]][rsts_ind[i[1]]] = i[2]
	# # print(mat)

	# #subtracting the average of each user from respective ratings

	# avgs=[]
	# for i in range(len(mat)):
	#     av = 0.0
	#     tot = 0
	#     for j in mat[i]:
	#         if j != -10:
	#             av = av + j
	#             tot += 1
	#     if(tot != 0):
	#         av = av / tot
	#         avgs.append(av)
	#         for j in range(len(mat[i])):
	#             if mat[i][j] != -10:
	#                 mat[i][j] = mat[i][j] - av


	# #all root of square sum
	# root_sqs=[]
	# for i in mat:
	#     sqs = 0
	#     for j in i:
	#         if j != -10:
	#             sqs = sqs + j*j
	#     root_sqs.append(math.sqrt(sqs))

	# #cosine relation of activ user with every other user
	# all_similr=[]
	# ans = []

	# for i in range(len(mat)):
	#     val = 0
	#     if activ == i:
	#         continue
	#     for j in range(len(mat[i])):
	#         if mat[i][j] != -10 and mat[activ][j] != -10:
	#             val = val + mat[i][j]*mat[activ][j]

	#     if(root_sqs[i] != 0 and val != 0 and root_sqs[activ] != 0):    
	#         val = val / (root_sqs[activ]*root_sqs[i])
	#         all_similr.append([val, i])

	# if len(all_similr) != 0:
	#     all_similr.sort()
	#     all_similr.reverse() #now it has all relations in decending order
	#     # print(all_similr)

	#     for j in range(len(mat[activ])):
	#         if mat[activ][j] != -10:#already there
	#             continue
	#         predic = avgs[activ]
	#         item = j
	#         tot = 0
	#         val = 0
	#         for i in all_similr:
	#             usr = i[1]
	#             if mat[usr][item] != -10:
	#                 val += mat[usr][item]*i[0]
	#                 #print(usr)
	#             tot += i[0]

	#         predic += (val / tot)
	#         if predic >= 2.1:
	#             ans.append(j)
	#             # print(predic)

	#     if len(ans) == 0:   #if no similar user rated this item then not possible or if users found but no item had sufficiently big predicted value
	#         ans.append(0)
	#         ans.append(1)
	#         ans.append(2)
	#         ans.append(3)
	        
	# else:       ##in case not possible if no similar users found
	#     ans.append(0)
	#     ans.append(1)
	#     ans.append(2)
	#     ans.append(3)
	    
	# print(ans)  ##here is final list of indexes############
	# final_lst=[]
	# for i in ans:
	#     final_lst.append(rsts[i])
	# print(final_lst)


	# final_restaurant_list = []
	# for restaurant in final_lst:
	# 	a = Restaurant.objects.filter(name=restaurant)
	# 	final_restaurant_list.append(a)

	# userid = request.session['userid']
	# user = User.objects.filter(id=request.session['userid'])

	# print final_restaurant_list
	# print final_hotel_list

	context_list = {
		'rest_one': rest_one,
		'rest_two': rest_two,
		'rest_three':rest_three,
		'rest_four':rest_four,
		'rest_five':rest_five,
		'hotel_one': hotel_one,
		'hotel_two': hotel_two,
		'hotel_three': hotel_three,
		'hotel_four': hotel_four,
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
	review_list = []
	for rate_review in detail:
		temp = []
		names = str(rate_review.item_name)
		names= names.replace(" ","")
		if names in name:
			rate_review_object.append(rate_review)
			temp.append(rate_review)
			print "username for review"
			usr =  rate_review.user.all()
			temp.append(usr[0].username)
		review_list.append(temp)
	rate_review_object.reverse()
	date = datetime.date.today()
	if flag == 1:
		img = place.menu
		img = str(img)
		img1 = img.split('_')
		img = img1[0]
		img = img[1:]
		if len(img1) != 1:
			img = img + '.jpg' 
		place.menu = img[1:]
		print place.menu
	if rate_review_object:
		context_list={
			'place' : place,
			'category' : category,
			'tags':tags_places,
			'related_places': related_places[:3],
			'rate_review':rate_review_object,
			'date':date,
			'flag':flag,
		}
	else:
		context_list={
			'place' : place,
			'tags':tags_places,
			'category' : category,
			'related_places': related_places[:3],
			'date':date,
			'flag': flag,
			# 'rate_review':rate_review_object,
		}
	return render(request,'product_detail.html',context_list)

def add_review(request,name):
	related_name=name
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
	pplace = Restaurant.objects.filter(name=name)
	flag=0
	if not pplace:
		pplace = Hotel.objects.filter(name=name)
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

	print pplace,new_review.review,name
	rate_review = Rate_Review.objects.filter(item_name=name)
	img = pplace[0].image
	img = str(img)
	img1 = img.split('_')
	img = img1[0]
	img = img[1:]
	if len(img1) != 1:
		img = img + '.jpg' 
		# print img
		pplace[0].image = img[1:]
	print pplace[0].image
	tags = []
	if flag==0:
		tags = str(pplace[0].cuisines).split(',')
	else:
		tags = str(pplace[0].hotel_tags).split(',')

	restaurants = Restaurant.objects.order_by('rating')
	print name
	restaurant_cuisine = []
	restaurant_list=[]
	related_places = []
	tags_places = []
	name = name.replace(" ","")
	for restaurant in restaurants:
		tags_all = []
		names = str(restaurant.name)
		names = names.replace(" ","")
		restaurant_list.append(restaurant)
		print name
		print names
		if name in names:
			flag=1
			
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
	# print rate_review
	print related_places
	# related_places = list(set(related_places))
	context_list = {
		'place':pplace[0],
		'rate_review':rate_review,
		'tags':tags,
		'related_places': related_places,
	}
	return render(request,'review.html',context_list)


def search(request):
	search_query = request.GET.get('search')
	city = request.GET.get('country')
	restaurant_list = Restaurant.objects.order_by('rating')
	hotel_list = Hotel.objects.order_by('rating')
	search_query = str(search_query)
	search_query = search_query.lower()
	print "search query"
	print search_query
	print "city"
	print city
	item_list = []
	flag=0
	if city=="-1":
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

	elif search_query == "":
		city = city.lower()
		restaurants = Restaurant.objects.all()
		for restaurant in restaurants:
			if city == restaurant.city.lower():
				item_list.append(restaurant)
		hotels = Hotel.objects.all()
		for hotel in hotels:
			if hotel.city.lower() == city:
				item_list.append(hotel)

	else:
		city = city.lower()
		for restaurant in restaurant_list:
			if city == restaurant.city.lower():
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
					if hotel.city.lower() == city:
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
    return HttpResponseRedirect('/')
 
def contact_us(request):
	context_list={}
	return render(request,'contact.html',context_list)

def about_us(request):
	context_list = {}
	return render(request,'about.html',context_list)