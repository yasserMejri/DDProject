# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.safestring import SafeString
from django.urls import reverse

from delivery import models as d_models
from service import models as s_models
from service import widgets
from postman import views as pm_views

import json
import geocoder
import random
import qrcode
import qrtools

# Create your views here.

def confirm(user, oid):
	"""
		TODO:  current : confirm -> progress
		TODO:  before  : progress -> complete
	"""
	order = d_models.Order.objects.get(pk=int(oid))

	orders = {}
	try:
		orders = json.loads(user.userprofile.orders)
	except:
		orders = user.userprofile.orders

	from_user = None

	for order in orders['confirm']:
		if order['order'] == oid:
			orders['confirm'].remove(order)
			from_user = order['from']
			break

	if from_user:
		from_user = User.objects.get(pk=from_user)
	else:
		print 'ERROR: From User Empty! on "Confirm" action!'
		return False, 0

	d = {
		'order': oid, 
		'from': from_user.id
	}

	duplicate = 0

	try:
		test = orders['progress']
	except:
		orders['progress'] = []

	if d in orders['progress']:
		duplicate = duplicate + 1
		pass
	else:
		orders['progress'].append(d)
	user.userprofile.orders = json.dumps(orders)
	user.userprofile.save()


	orders = {}
	try:
		orders = json.loads(from_user.userprofile.orders)
	except:
		orders = from_user.userprofile.orders

	d = { }

	if from_user.userprofile.user_type.name != 'Client':

		for order in orders['progress']:
			if order['order'] == oid:
				d = order
				orders['progress'].remove(order)
				break

		try:
			test = orders['complete']
		except:
			orders['complete'] = []

		if d in orders['complete']:
			duplicate = duplicate + 2
			pass
		else:
			orders['complete'].append(d)
		from_user.userprofile.orders = json.dumps(orders)
		from_user.userprofile.save()

	return True, duplicate


def next(user, oid, nid):
	"""
		TODO:  next : confirm
	"""
	order = d_models.Order.objects.get(pk=oid)
	next_user = User.objects.get(pk=nid)

	orders = {}
	try:
		orders = json.loads(next_user.userprofile.orders)
	except:
		orders = next_user.userprofile.orders

	d = {
		'order': oid, 
		'from': user.id
	}

	duplicate = False
	
	try:
		test = orders['confirm']
	except:
		orders['confirm'] = []

	if d in orders['confirm']:
		duplicate = True
		pass
	else:
		orders['confirm'].append(d)
	next_user.userprofile.orders = json.dumps(orders)
	next_user.userprofile.save()

	return True, duplicate


@login_required
def register_order(request):

	"""
		confirm action:
		Scan QR code and register onto orders list of process center
	"""

	order = data = fee_total = msg = msg_type = None

	if request.method == 'POST':
		oid = request.POST.get('oid')
		if oid:

			confirm(request.user, oid)

			order = d_models.Order.objects.get(pk=int(oid))
			data = json.loads(order.data)
			user = request.user

			return render(request, 'pcenter/order_register.html', {
				'user': request.user, 
				'order': order,
				'data': data, 
				'countries': widgets.COUNTRY_CHOICES, 
				'fee_total': fee_total, 
				'msg' : msg, 
				'msg_type': msg_type, 
				'close': True
				})


		qrcode_img = request.FILES['qrcode']

		qr = qrtools.QR()
		try:
			qr.decode(qrcode_img)
			qr_data = json.loads(qr.data)

			order = d_models.Order.objects.get(pk=qr_data['id'])
			if order.id != int(request.GET.get('order')):
				raise NameError('No matching')
			data = json.loads(order.data)
			fee_total = 0;
			for item in data['documents']:
				fee_total = fee_total + item['fee']
		except:
			order = None
			msg = 'QR Code Incorrect!'
			msg_type = 'danger'

	return render(request, 'pcenter/order_register.html', {
		'user': request.user, 
		'order': order,
		'data': data, 
		'countries': widgets.COUNTRY_CHOICES, 
		'fee_total': fee_total, 
		'msg' : msg, 
		'msg_type': msg_type
		})

@login_required
def confirm_order(request):
	"""
		When next part receives and confirms the order once more confirm for source part for handshake action
	"""

	if request.method == 'GET':
		return HttpResponse('Post only')

	o_id = request.POST.get('o_id')

	confirm(request.user, o_id)

	return HttpResponse(json.dumps({
		'status': 'success', 
		'request': request.POST
		}))

@login_required
def confirm_order_bulk(request):
	if request.method == 'GET':
		return HttpResponse('Post only')

	payload = json.loads(request.POST.get('payload'))
	for o_id in payload:
		confirm(request.user, str(o_id))

	return HttpResponse(json.dumps({
		'status': 'success', 
		'request': request.POST
		}))

@login_required
def order_list(request):

	user = request.user

	u_orders_ = []
	u_orders = {}
	try:
		u_orders_ = json.loads(user.userprofile.orders)
	except:
		u_orders_ = user.userprofile.orders

	for idx in u_orders_:
		orders = u_orders_[idx]
		u_orders[idx] = []
		for data in orders:
			order = d_models.Order.objects.get(pk=int(data['order']))
			u_orders[idx].append({
				'from': User.objects.get(pk=int(data['from'])), 
				'order': order, 
				'next': pm_views.find_next_dest(user.id, order.id)
				})

	orders_ = d_models.Order.objects.all()
	orders = []
	cur_pc = pm_views.find_next_dest(request.user.id, orders_[0].id)
	for order in orders_:
		orders.append({
			'order': order, 
			'next': pm_views.find_next_dest(user.id, order.id)
			}) 

	return render(request, 'pcenter/order_list.html', {
		'user': request.user, 
		'orders': u_orders, 
		'all_orders': orders, 
		'cur_pc': cur_pc
		})

def order_next_manage(request, next_id, o_id):

	status, duplicate = next(request.user, o_id, next_id)

	if duplicate:
		return HttpResponse(json.dumps({
			'status': 'warning',
			'msg': 'Already Exists On Process Center', 
			'msg_type': 'warning'
			}))
	else:
		return HttpResponse(json.dumps({
			'status': 'success'
			}))

@login_required
def order_next(request):
	if request.method == 'GET':
		return HttpResponse('Post only')
	next_id = request.POST.get('next_id')
	o_id = request.POST.get('order_id')

	return order_next_manage(request, next_id, o_id)


@login_required
def order_next_bulk(request):
	if request.method == 'GET':
		return HttpResponse('Post only')
	data = json.loads(request.POST.get('payload'))
	for item in data:
		order_next_manage(request, item['next_id'], item['order_id'])

	return HttpResponse(json.dumps({
		'status': 'success'
		}))
