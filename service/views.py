# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from service import models

import json

# Create your views here.

@login_required
def service_autocomplete(request):
	if request.method == "GET":
		return HttpResponse("POST only")

	s_id = int(request.POST.get('service_id'))
	keyword = request.POST.get('keyword')
	field_here = request.POST.get('field')
	all_data = request.POST.get('all')

	service = models.Service.objects.get(pk=s_id)
	service_data = service.data
	field_data = service.fields

	target_field = {}

	loc_fields = []
	for field in field_data:
		if field['location'] == True:
			loc_fields.append(field)
		if field['v_name'] == field_here:
			target_field = field

	location_data = models.SupportedLocation.objects.filter(service = service)
	if len(location_data) != 0:
		location_data = location_data[0].locations
	else:
		location_data = []


	print '_________________________________________________'
	print target_field
	print '_________________________________________________'


	result = {}

	result[service.itemName] = []

	for item in service_data:
		if str(item[target_field['v_name']]).find(keyword) != -1:
			result[service.itemName].append(item)
			if all_data == 'true':
				for location in location_data:
					# location = location_data[lid]
					yes = True
					for loc_field in loc_fields:
						# loc_field = loc_fields[fid]
						if location[loc_field['v_name']] != item[loc_field['v_name']]:
							yes = False
							break
					if yes:
						result['location'] = location
						break

	return HttpResponse(json.dumps(result))
