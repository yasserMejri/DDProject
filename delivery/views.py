# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import SafeString

from service import widgets
from delivery import models
from service import models as s_models
from postman import views as pm_views

import json

# Create your views here.

def index(request):
	return render(request, 'main.html', {
		'user': request.user, 
		})

def d_login(request):
	error = ''
	if request.method == 'POST':
		try:
			username = User.objects.get(email=request.POST.get('email')).username
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('home'))
			error = "Password Incorrect!"

		except:
			error = 'No Such User!'

	return render(request, 'login.html', {
		'user': request.user, 
		'error': error
		})

def d_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))

def register(request):

	msg = ''
	msg_type = ''

	if request.method == 'POST':
		user = None
		profile = None
		try:
			email = request.POST.get('email')
			password = request.POST.get('password')
			firstname = request.POST.get('firstname')
			lastname = request.POST.get('lastname')

			phone = request.POST.get('phone')
			fax = request.POST.get('fax')
			company = request.POST.get('company')
			address = request.POST.get('address')
			postcode = request.POST.get('postcode')
			country = request.POST.get('country')

			if len(User.objects.filter(email=email)) > 0:
				msg = 'Email already used. Please try again with different email'
				msg_type = 'danger'
			user = User(
				username=email,
				email=email,
				first_name = firstname,
				last_name = lastname
				)
			user.save()
			user.set_password(password)
			user.save()
			profile = models.UserProfile(
				user=user, 
				phone=phone,
				fax=fax,
				company=company,
				address=address,
				postcode=postcode,
				country=country
				)
			profile.save()
		except:
			if user:
				user.delete()
			if profile:
				profile.delete()
		return HttpResponseRedirect(reverse('login'))

	countries = widgets.COUNTRY_CHOICES
	return render(request, 'register.html', {
		'countries': countries, 
		'msg': msg, 
		'msg_type': msg_type
		})

@login_required
def new_order(request):

	superservices = s_models.SuperService.objects.all()

	service_fields = {}

	if request.method == 'POST':
		order = models.Order(
			user = request.user,
			data = request.POST.get('order-data'),
			status = models.OrderStatus.objects.get(pk=1), 
			priority = models.OrderPriority.objects.get(pk=1)
			)
		order.save()
		order.generate_qrcode();
		order.save()

		nxt_postman = pm_views.find_next_dest(request.user.id, order.id)

		try:
			orders = json.loads(nxt_postman.userprofile.orders)
		except:
			orders = nxt_postman.userprofile.orders

		try:
			orders['confirm'].insert(0, {
				'order': str(order.id), 
				'from': request.user.id
				})
		except:
			orders['confirm'] = []
			orders['confirm'].insert(0, {
				'order': str(order.id), 
				'from': request.user.id
				})
		nxt_postman.userprofile.orders = json.dumps(orders)
		nxt_postman.userprofile.save()

		track = models.Track(
			from_user = request.user, 
			to_user = nxt_postman, 
			order = order, 
			description = "Order Created"
			)
		track.save()

		return HttpResponseRedirect(reverse('order_review', kwargs={'pk':order.id}))

	for superservice in superservices:
		services = s_models.Service.objects.filter(superservice = superservice)
		service_fields[superservice.id] = {}
		service_fields[superservice.id]['name'] = superservice.name
		service_fields[superservice.id]['services'] = {}
		for service in services:
			subservices = s_models.SubService.objects.filter(service=service)
			service_fields[superservice.id]['services'][service.id] = {}
			service_fields[superservice.id]['services'][service.id]['id'] = service.id
			service_fields[superservice.id]['services'][service.id]['name'] = service.name
			service_fields[superservice.id]['services'][service.id]['itemName'] = service.itemName
			service_fields[superservice.id]['services'][service.id]['fields'] = service.fields
			service_fields[superservice.id]['services'][service.id]['subservices'] = {}
			for subservice in subservices:
				service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id] = {}
				service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id]['name'] = subservice.name
				service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id]['checklist'] = {}
				checklists = s_models.CheckList.objects.filter(service=subservice)
				for checklist in checklists:
					service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id]['checklist'][checklist.id] = {}
					service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id]['checklist'][checklist.id]['no'] = checklist.id
					# service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id]['checklist'][checklist.id]['name'] = checklist.name
					service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id]['checklist'][checklist.id]['document'] = checklist.document
					service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id]['checklist'][checklist.id]['quantity'] = checklist.quantity
					service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id]['checklist'][checklist.id]['unit_price'] = checklist.unit_price
					service_fields[superservice.id]['services'][service.id]['subservices'][subservice.id]['checklist'][checklist.id]['fee'] = checklist.fee



	return render(request, 'new_order.html', {
		'countries': widgets.COUNTRY_CHOICES, 
		'user': request.user, 
		'superservices':  superservices, 
		'service_fields': SafeString(json.dumps(service_fields))
		})

@login_required
def order_review(request, pk):

	order = models.Order.objects.get(pk=pk)

	data = json.loads(order.data)
	fee_total = 0;
	for item in data['documents']:
		fee_total = fee_total + item['fee']

	return render(request, 'order_review.html', {
		'order': order, 
		'user': request.user, 
		'data': data, 
		'countries': widgets.COUNTRY_CHOICES, 
		'js_string': SafeString((order.data)), 
		'fee_total': fee_total
		})

@login_required
def order_list(request):

	orders = models.Order.objects.filter(user=request.user).order_by('-creationdate')

	keys = ['sent','confirm', 'progress', 'received','complete']

	try:
		u_orders = json.loads(request.user.userprofile.orders)
	except:
		u_orders = request.user.userprofile.orders

	for key in u_orders:
		idx = 0
		for val in u_orders[key]:
			u_orders[key][idx]['order'] = models.Order.objects.get(pk=int(val['order']))
			if key != 'complete' and key != 'progress':
				u_orders[key][idx]['from'] = User.objects.get(pk=int(val['from']))
			idx = idx + 1
	u_orders['sent'] = []
	for order in orders:
		u_orders['sent'].append({
			'order': order,
			'from': None
			})

	keyorder = ['sent','confirm', 'progress', 'received','complete']

	return render(request, 'order_list.html', {
		'user': request.user,
		'orders': [], 
		'u_orders': u_orders,
		'keyorder': keyorder
		})

@login_required
def order_confirm(request, oid, uid):

	user = request.user
	order = models.Order.objects.get(pk=oid)
	before = User.objects.get(pk=uid)

	data = json.loads(order.data)
	fee_total = 0;
	for item in data['documents']:
		fee_total = fee_total + item['fee']

	if request.method=="POST":
		# Find order from Client's 'confirm' list and mark as 'received'


		orders = []
		try:
			orders = json.loads(order.user.userprofile.orders)
		except:
			orders = order.user.userprofile.orders

		try:
			orders['complete'].insert(0, {
				'order': order.id,
				'from': None
				})
		except:
			orders['complete'] = []
			orders['complete'].insert(0, {
				'order': order.id,
				'from': None
				})

		for order in orders['progress']:
			if order['order'] == oid:
				order['progress'].remove(order)
				break

		order.user.userprofile.orders = json.dumps(orders)
		order.user.userprofile.save()

		orders = []
		try:
			orders = json.loads(user.userprofile.orders)
		except:
			orders = user.userprofile.orders

		for order in orders['confirm']:
			if order['order'] == oid:
				orders['confirm'].remove(order)
				try:
					orders['received'].insert(0, order)
				except:
					orders['received'] = []
					orders['received'].insert(0, order)
				break

		user.userprofile.orders = json.dumps(orders)
		user.userprofile.save()

		# Find order in Postman's 'progress' list and mark as 'complete'
		orders = []

		try:
			orders = json.loads(before.userprofile.orders)
		except:
			orders = before.userprofile.orders

		for order in orders['progress']:
			if order['order'] == oid:
				orders['progress'].remove(order)
				try:
					orders['complete'].insert(0, order)
				except:
					orders['complete'] = []
					orders['complete'].insert(0, order)
				break
		before.userprofile.orders = json.dumps(orders)
		before.userprofile.save()

		return HttpResponseRedirect(reverse('order_list'))

	return render(request, 'order_confirm.html', {
		'order': order, 
		'user': request.user, 
		'data': data, 
		'countries': widgets.COUNTRY_CHOICES, 
		'js_string': SafeString((order.data)), 
		'fee_total': fee_total, 
		'from': before
		})

def order_track(request, oid):

	order = models.Order.objects.get(pk=oid)
	tracks = models.Track.objects.filter(order=order).order_by('time')

	return render(request, 'order_track.html', {
		'user': request.user, 
		'order': order, 
		'tracks': tracks
		})
