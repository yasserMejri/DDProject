from django import forms

from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.safestring import SafeString
from service import models

import json



COUNTRY_CHOICES ={
    'AF':"Afghanistan",
    'AX':"Aland Islands",
    'AL':"Albania",
    'DZ':"Algeria",
    'AS':"American Samoa",
    'AD':"Andorra",
    'AO':"Angola",
    'AI':"Anguilla",
    'AQ':"Antarctica",
    'AG':"Antigua and Barbuda",
    'AR':"Argentina",
    'AM':"Armenia",
    'AW':"Aruba",
    'AU':"Australia",
    'AT':"Austria",
    'AZ':"Azerbaijan",
    'BS':"Bahamas",
    'BH':"Bahrain",
    'BD':"Bangladesh",
    'BB':"Barbados",
    'BY':"Belarus",
    'BE':"Belgium",
    'BZ':"Belize",
    'BJ':"Benin",
    'BM':"Bermuda",
    'BT':"Bhutan",
    'BO':"Bolivia, Plurinational State of",
    'BQ':"Bonaire, Sint Eustatius and Saba",
    'BA':"Bosnia and Herzegovina",
    'BW':"Botswana",
    'BV':"Bouvet Island",
    'BR':"Brazil",
    'IO':"British Indian Ocean Territory",
    'BN':"Brunei Darussalam",
    'BG':"Bulgaria",
    'BF':"Burkina Faso",
    'BI':"Burundi",
    'KH':"Cambodia",
    'CM':"Cameroon",
    'CA':"Canada",
    'CV':"Cape Verde",
    'KY':"Cayman Islands",
    'CF':"Central African Republic",
    'TD':"Chad",
    'CL':"Chile",
    'CN':"China",
    'CX':"Christmas Island",
    'CC':"Cocos (Keeling) Islands",
    'CO':"Colombia",
    'KM':"Comoros",
    'CG':"Congo",
    'CD':"Congo, the Democratic Republic of the",
    'CK':"Cook Islands",
    'CR':"Costa Rica",
    'CI':"Cote d Ivoire",
    'HR':"Croatia",
    'CU':"Cuba",
    'CW':"Curacao",
    'CY':"Cyprus",
    'CZ':"Czech Republic",
    'DK':"Denmark",
    'DJ':"Djibouti",
    'DM':"Dominica",
    'DO':"Dominican Republic",
    'EC':"Ecuador",
    'EG':"Egypt",
    'SV':"El Salvador",
    'GQ':"Equatorial Guinea",
    'ER':"Eritrea",
    'EE':"Estonia",
    'ET':"Ethiopia",
    'FK':"Falkland Islands (Malvinas)",
    'FO':"Faroe Islands",
    'FJ':"Fiji",
    'FI':"Finland",
    'FR':"France",
    'GF':"French Guiana",
    'PF':"French Polynesia",
    'TF':"French Southern Territories",
    'GA':"Gabon",
    'GM':"Gambia",
    'GE':"Georgia",
    'DE':"Germany",
    'GH':"Ghana",
    'GI':"Gibraltar",
    'GR':"Greece",
    'GL':"Greenland",
    'GD':"Grenada",
    'GP':"Guadeloupe",
    'GU':"Guam",
    'GT':"Guatemala",
    'GG':"Guernsey",
    'GN':"Guinea",
    'GW':"Guinea-Bissau",
    'GY':"Guyana",
    'HT':"Haiti",
    'HM':"Heard Island and McDonald Islands",
    'VA':"Holy See (Vatican City State)",
    'HN':"Honduras",
    'HK':"Hong Kong",
    'HU':"Hungary",
    'IS':"Iceland",
    'IN':"India",
    'ID':"Indonesia",
    'IR':"Iran, Islamic Republic of",
    'IQ':"Iraq",
    'IE':"Ireland",
    'IM':"Isle of Man",
    'IL':"Israel",
    'IT':"Italy",
    'JM':"Jamaica",
    'JP':"Japan",
    'JE':"Jersey",
    'JO':"Jordan",
    'KZ':"Kazakhstan",
    'KE':"Kenya",
    'KI':"Kiribati",
    'KP':"Korea, Democratic People`s Republic of",
    'KR':"Korea, Republic of",
    'KW':"Kuwait",
    'KG':"Kyrgyzstan",
    'LA':"Lao People s Democratic Republic",
    'LV':"Latvia",
    'LB':"Lebanon",
    'LS':"Lesotho",
    'LR':"Liberia",
    'LY':"Libya",
    'LI':"Liechtenstein",
    'LT':"Lithuania",
    'LU':"Luxembourg",
    'MO':"Macao",
    'MK':"Macedonia, the former Yugoslav Republic of",
    'MG':"Madagascar",
    'MW':"Malawi",
    'MY':"Malaysia",
    'MV':"Maldives",
    'ML':"Mali",
    'MT':"Malta",
    'MH':"Marshall Islands",
    'MQ':"Martinique",
    'MR':"Mauritania",
    'MU':"Mauritius",
    'YT':"Mayotte",
    'MX':"Mexico",
    'FM':"Micronesia, Federated States of",
    'MD':"Moldova, Republic of",
    'MC':"Monaco",
    'MN':"Mongolia",
    'ME':"Montenegro",
    'MS':"Montserrat",
    'MA':"Morocco",
    'MZ':"Mozambique",
    'MM':"Myanmar",
    'NA':"Namibia",
    'NR':"Nauru",
    'NP':"Nepal",
    'NL':"Netherlands",
    'NC':"New Caledonia",
    'NZ':"New Zealand",
    'NI':"Nicaragua",
    'NE':"Niger",
    'NG':"Nigeria",
    'NU':"Niue",
    'NF':"Norfolk Island",
    'MP':"Northern Mariana Islands",
    'NO':"Norway",
    'OM':"Oman",
    'PK':"Pakistan",
    'PW':"Palau",
    'PS':"Palestinian Territory, Occupied",
    'PA':"Panama",
    'PG':"Papua New Guinea",
    'PY':"Paraguay",
    'PE':"Peru",
    'PH':"Philippines",
    'PN':"Pitcairn",
    'PL':"Poland",
    'PT':"Portugal",
    'PR':"Puerto Rico",
    'QA':"Qatar",
    'RE':"Reunion",
    'RO':"Romania",
    'RU':"Russian Federation",
    'RW':"Rwanda",
    'BL':"Saint Barthelemy",
    'SH':"Saint Helena, Ascension and Tristan da Cunha",
    'KN':"Saint Kitts and Nevis",
    'LC':"Saint Lucia",
    'MF':"Saint Martin (French part)",
    'PM':"Saint Pierre and Miquelon",
    'VC':"Saint Vincent and the Grenadines",
    'WS':"Samoa",
    'SM':"San Marino",
    'ST':"Sao Tome and Principe",
    'SA':"Saudi Arabia",
    'SN':"Senegal",
    'RS':"Serbia",
    'SC':"Seychelles",
    'SL':"Sierra Leone",
    'SG':"Singapore",
    'SX':"Sint Maarten (Dutch part)",
    'SK':"Slovakia",
    'SI':"Slovenia",
    'SB':"Solomon Islands",
    'SO':"Somalia",
    'ZA':"South Africa",
    'GS':"South Georgia and the South Sandwich Islands",
    'SS':"South Sudan",
    'ES':"Spain",
    'LK':"Sri Lanka",
    'SD':"Sudan",
    'SR':"Suriname",
    'SJ':"Svalbard and Jan Mayen",
    'SZ':"Swaziland",
    'SE':"Sweden",
    'CH':"Switzerland",
    'SY':"Syrian Arab Republic",
    'TW':"Taiwan, Province of China",
    'TJ':"Tajikistan",
    'TZ':"Tanzania, United Republic of",
    'TH':"Thailand",
    'TL':"Timor-Leste",
    'TG':"Togo",
    'TK':"Tokelau",
    'TO':"Tonga",
    'TT':"Trinidad and Tobago",
    'TN':"Tunisia",
    'TR':"Turkey",
    'TM':"Turkmenistan",
    'TC':"Turks and Caicos Islands",
    'TV':"Tuvalu",
    'UG':"Uganda",
    'UA':"Ukraine",
    'AE':"United Arab Emirates",
    'GB':"United Kingdom",
    'US':"United States",
    'UM':"United States Minor Outlying Islands",
    'UY':"Uruguay",
    'UZ':"Uzbekistan",
    'VU':"Vanuatu",
    'VE':"Venezuela, Bolivarian Republic of",
    'VN':"Viet Nam",
    'VG':"Virgin Islands, British",
    'VI':"Virgin Islands, U.S.",
    'WF':"Wallis and Futuna",
    'EH':"Western Sahara",
    'YE':"Yemen",
    'ZM':"Zambia",
    'ZW':"Zimbabwe"
}



class FieldWidget(forms.Widget):
	template_name = 'widgets/field.html'
	# fields is for detecting field name, type, pre-select options and etc
	fields = [
		{
			'name': 'name', 
			'type': 'text'
		}, {
			'name': 'type', 
			'type': 'select', 
			'value':['text','select','checkbox']
		}, {
			'name': 'value', 
			'type': 'text'
		}, {
			'name': 'placeholder', 
			'type': 'text'
		}, {
			'name': 'location',
			'type': 'checkbox'
		}]

	def render(self, name, value, attrs=None):
		if value == {}:
			value = []
		context = {
			'name': name, 
			'value': value, 
			'fields': SafeString(json.dumps(self.fields)), 
			'js_string': SafeString(json.dumps(value))
		}
		return mark_safe(render_to_string(self.template_name, context))

class DataWidget(forms.Widget):
	template_name = 'widgets/data.html'

	def render(self, name, value, attrs=None):
		if value == {}:
			value = []
		context = {
			'name': name, 
			'value': value, 
			'js_string': SafeString(json.dumps(value))
		}
		return mark_safe(render_to_string(self.template_name, context))

class LocationWidget(forms.Widget):
	template_name = 'widgets/location.html'
	fields = [ 'name', 'address', 'post', 'country', 'email', 'phone', 'fax' ]

	def render(self, name, value, attrs=None):
		loc_fields = [ [item.id, item.fields] for item in models.Service.objects.all() ]
		i_field = {}
		for idx, fields in loc_fields:
			i_field[idx] = []
			for field in fields:
				print field
				print '_________________________----'
				if field['location'] == True:
					i_field[idx].append(field)

		print i_field

		if value == {}:
			value = []
		context = {
			'name': name, 
			'value': value, 
			'js_string': SafeString(json.dumps(value)), 
			'countries': SafeString(json.dumps(COUNTRY_CHOICES)), 
			'fields': SafeString(json.dumps(self.fields)), 
			'loc_fields': SafeString(json.dumps(i_field))
		}
		return mark_safe(render_to_string(self.template_name, context))
