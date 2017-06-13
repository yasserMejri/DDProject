# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from delivery import models as d_models

# Create your models here.

class Orders(models.Model):
	order = models.ForeignKey(d_models.Order, related_name='pcenter_order')
	prv_node = models.ForeignKey(User, related_name='pcenter_prv_node')
	nxt_node = models.ForeignKey(User, related_name='pcenter_nxt_node')
	is_complete = models.BooleanField(default=False)
	is_confirmed = models.BooleanField(default=False)
	pcenter = models.ForeignKey(User, related_name='pcenter') #Process center who processes this order
	group = models.IntegerField()

	def __str__(self):
		status_string = ''
		if is_confirmed and is_complete:
			status_string = 'completed'
		if (is_complete or is_confirmed) == False:
			status_string = 'pending'
		if is_confirmed == True and is_complete == False:
			status_string = 'processing'
		if is_complete == True and is_confirmed == False:
			status_string = "INVALID STATUS"
		return 'Order #' + str(self.order.id ) + ' ' + status_string + ' on Process center ' + pcenter.id
