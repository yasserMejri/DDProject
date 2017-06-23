# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms

from service import models
from service import widgets

# Register your models here.

class CheckList(admin.TabularInline):
	model = models.CheckList

class SubServiceAdmin(admin.ModelAdmin):
	model = models.SubService
	inlines = [
		CheckList
	]

class ServiceForm(forms.ModelForm):
	class Meta:
		model = models.Service
		fields = '__all__'
		widgets = {
			'fields': widgets.FieldWidget, 
			'data': widgets.DataWidget
		}

class ServiceAdmin(admin.ModelAdmin):
	form = ServiceForm

class SupportedLocationForm(forms.ModelForm):
	class Meta:
		model = models.SupportedLocation
		fields = '__all__'
		widgets = {
			'locations': widgets.LocationWidget
		}

class SupportedLocationAdmin(admin.ModelAdmin):
	form = SupportedLocationForm

admin.site.register(models.SuperService)

admin.site.register(models.Service, ServiceAdmin)

admin.site.register(models.SubService, SubServiceAdmin)

admin.site.register(models.SupportedLocation, SupportedLocationAdmin)

