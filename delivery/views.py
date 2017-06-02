# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.

def index(request):
	return render(request, 'main.html', {
		'user': request.user
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
	return render(request, 'register.html')

def new_order(request):
	return render(request, 'new_order.html', {
		'user': request.user, 
		})
