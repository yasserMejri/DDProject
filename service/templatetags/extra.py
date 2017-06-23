from django.template.defaulttags import register

from service import widgets

import json


@register.filter
def get_item(dictionary, key):
	try:
		return dictionary.get(key)
	except:
		return []

def get_value_list(value):
	data = ''
	key = ''
	if isinstance(value, dict):
		for key_item in value.keys():

			if isinstance(value[key_item], dict):
				k, d = get_value_list(value[key_item])
				key = key + '?' + k
				data = data + '?' + d
			elif isinstance(value[key_item], list):
				for item in value[key_item]:
					k, d = get_value_list(item)
					key = key + '?' + k
					data = data + '?' + d
			else:
				try:
					k, d = get_value_list(json.loads(value[key_item]))
					key = key + '?' + k
					data = data + '?' + d
				except:
					key = key + '?' + key_item
					if isinstance(value[key_item], bool):
						data = data + '?'+key_item
					else:
						if key_item == 'country':
							try:
								data = data+'?'+widgets.COUNTRY_CHOICES[value[key_item]]
							except:
								data = data+'?'+''
						else:
							data = data + '?' + str(value[key_item])

	return key, data

@register.filter
def get_full_content(order):
	try:

		all_data = json.loads(order.data)
		key, data = get_value_list(all_data)

		return order.__str__()+'?'+data
	except:

		return 'Error'