# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import jsonfield

# Create your models here.

class SuperService(models.Model):
	name = models.CharField(max_length=20)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name

class Service(models.Model):
	name = models.CharField(max_length=50)
	itemName = models.CharField(max_length=50)
	fields = jsonfield.JSONField()
	data = jsonfield.JSONField()
	description = models.TextField(null=True, blank=True)
	superservice = models.ForeignKey(SuperService, null=True, default=None)

	def __str__(self):
		return self.name + " - " + self.itemName + " :  " + self.superservice.name

class CheckList(models.Model):
	name =models.CharField(max_length = 100)
	description = models.TextField()
	quantity = models.IntegerField()
	service = models.ForeignKey('SubService')
	unit_price = models.IntegerField()
	fee = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class SubService(models.Model):
	name = models.CharField(max_length=50)
	service = models.ForeignKey(Service)

	def __str__(self):
		return self.name

class SupportedLocation(models.Model):
	service = models.ForeignKey(Service, null=True)
	locations = jsonfield.JSONField()

	def __str__(self):
		return self.service.name
