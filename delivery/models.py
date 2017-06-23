from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from location_field.models.plain import PlainLocationField
import qrcode
import StringIO
import jsonfield
import json


COUNTRY_CHOICES =(
    ('AF',"Afghanistan"),
    ('AX',"Aland Islands"),
    ('AL',"Albania"),
    ('DZ',"Algeria"),
    ('AS',"American Samoa"),
    ('AD',"Andorra"),
    ('AO',"Angola"),
    ('AI',"Anguilla"),
    ('AQ',"Antarctica"),
    ('AG',"Antigua and Barbuda"),
    ('AR',"Argentina"),
    ('AM',"Armenia"),
    ('AW',"Aruba"),
    ('AU',"Australia"),
    ('AT',"Austria"),
    ('AZ',"Azerbaijan"),
    ('BS',"Bahamas"),
    ('BH',"Bahrain"),
    ('BD',"Bangladesh"),
    ('BB',"Barbados"),
    ('BY',"Belarus"),
    ('BE',"Belgium"),
    ('BZ',"Belize"),
    ('BJ',"Benin"),
    ('BM',"Bermuda"),
    ('BT',"Bhutan"),
    ('BO',"Bolivia, Plurinational State of"),
    ('BQ',"Bonaire, Sint Eustatius and Saba"),
    ('BA',"Bosnia and Herzegovina"),
    ('BW',"Botswana"),
    ('BV',"Bouvet Island"),
    ('BR',"Brazil"),
    ('IO',"British Indian Ocean Territory"),
    ('BN',"Brunei Darussalam"),
    ('BG',"Bulgaria"),
    ('BF',"Burkina Faso"),
    ('BI',"Burundi"),
    ('KH',"Cambodia"),
    ('CM',"Cameroon"),
    ('CA',"Canada"),
    ('CV',"Cape Verde"),
    ('KY',"Cayman Islands"),
    ('CF',"Central African Republic"),
    ('TD',"Chad"),
    ('CL',"Chile"),
    ('CN',"China"),
    ('CX',"Christmas Island"),
    ('CC',"Cocos (Keeling) Islands"),
    ('CO',"Colombia"),
    ('KM',"Comoros"),
    ('CG',"Congo"),
    ('CD',"Congo, the Democratic Republic of the"),
    ('CK',"Cook Islands"),
    ('CR',"Costa Rica"),
    ('CI',"Cote d'Ivoire"),
    ('HR',"Croatia"),
    ('CU',"Cuba"),
    ('CW',"Curacao"),
    ('CY',"Cyprus"),
    ('CZ',"Czech Republic"),
    ('DK',"Denmark"),
    ('DJ',"Djibouti"),
    ('DM',"Dominica"),
    ('DO',"Dominican Republic"),
    ('EC',"Ecuador"),
    ('EG',"Egypt"),
    ('SV',"El Salvador"),
    ('GQ',"Equatorial Guinea"),
    ('ER',"Eritrea"),
    ('EE',"Estonia"),
    ('ET',"Ethiopia"),
    ('FK',"Falkland Islands (Malvinas)"),
    ('FO',"Faroe Islands"),
    ('FJ',"Fiji"),
    ('FI',"Finland"),
    ('FR',"France"),
    ('GF',"French Guiana"),
    ('PF',"French Polynesia"),
    ('TF',"French Southern Territories"),
    ('GA',"Gabon"),
    ('GM',"Gambia"),
    ('GE',"Georgia"),
    ('DE',"Germany"),
    ('GH',"Ghana"),
    ('GI',"Gibraltar"),
    ('GR',"Greece"),
    ('GL',"Greenland"),
    ('GD',"Grenada"),
    ('GP',"Guadeloupe"),
    ('GU',"Guam"),
    ('GT',"Guatemala"),
    ('GG',"Guernsey"),
    ('GN',"Guinea"),
    ('GW',"Guinea-Bissau"),
    ('GY',"Guyana"),
    ('HT',"Haiti"),
    ('HM',"Heard Island and McDonald Islands"),
    ('VA',"Holy See (Vatican City State)"),
    ('HN',"Honduras"),
    ('HK',"Hong Kong"),
    ('HU',"Hungary"),
    ('IS',"Iceland"),
    ('IN',"India"),
    ('ID',"Indonesia"),
    ('IR',"Iran, Islamic Republic of"),
    ('IQ',"Iraq"),
    ('IE',"Ireland"),
    ('IM',"Isle of Man"),
    ('IL',"Israel"),
    ('IT',"Italy"),
    ('JM',"Jamaica"),
    ('JP',"Japan"),
    ('JE',"Jersey"),
    ('JO',"Jordan"),
    ('KZ',"Kazakhstan"),
    ('KE',"Kenya"),
    ('KI',"Kiribati"),
    ('KP',"Korea, Democratic People's Republic of"),
    ('KR',"Korea, Republic of"),
    ('KW',"Kuwait"),
    ('KG',"Kyrgyzstan"),
    ('LA',"Lao People's Democratic Republic"),
    ('LV',"Latvia"),
    ('LB',"Lebanon"),
    ('LS',"Lesotho"),
    ('LR',"Liberia"),
    ('LY',"Libya"),
    ('LI',"Liechtenstein"),
    ('LT',"Lithuania"),
    ('LU',"Luxembourg"),
    ('MO',"Macao"),
    ('MK',"Macedonia, the former Yugoslav Republic of"),
    ('MG',"Madagascar"),
    ('MW',"Malawi"),
    ('MY',"Malaysia"),
    ('MV',"Maldives"),
    ('ML',"Mali"),
    ('MT',"Malta"),
    ('MH',"Marshall Islands"),
    ('MQ',"Martinique"),
    ('MR',"Mauritania"),
    ('MU',"Mauritius"),
    ('YT',"Mayotte"),
    ('MX',"Mexico"),
    ('FM',"Micronesia, Federated States of"),
    ('MD',"Moldova, Republic of"),
    ('MC',"Monaco"),
    ('MN',"Mongolia"),
    ('ME',"Montenegro"),
    ('MS',"Montserrat"),
    ('MA',"Morocco"),
    ('MZ',"Mozambique"),
    ('MM',"Myanmar"),
    ('NA',"Namibia"),
    ('NR',"Nauru"),
    ('NP',"Nepal"),
    ('NL',"Netherlands"),
    ('NC',"New Caledonia"),
    ('NZ',"New Zealand"),
    ('NI',"Nicaragua"),
    ('NE',"Niger"),
    ('NG',"Nigeria"),
    ('NU',"Niue"),
    ('NF',"Norfolk Island"),
    ('MP',"Northern Mariana Islands"),
    ('NO',"Norway"),
    ('OM',"Oman"),
    ('PK',"Pakistan"),
    ('PW',"Palau"),
    ('PS',"Palestinian Territory, Occupied"),
    ('PA',"Panama"),
    ('PG',"Papua New Guinea"),
    ('PY',"Paraguay"),
    ('PE',"Peru"),
    ('PH',"Philippines"),
    ('PN',"Pitcairn"),
    ('PL',"Poland"),
    ('PT',"Portugal"),
    ('PR',"Puerto Rico"),
    ('QA',"Qatar"),
    ('RE',"Reunion"),
    ('RO',"Romania"),
    ('RU',"Russian Federation"),
    ('RW',"Rwanda"),
    ('BL',"Saint Barthelemy"),
    ('SH',"Saint Helena, Ascension and Tristan da Cunha"),
    ('KN',"Saint Kitts and Nevis"),
    ('LC',"Saint Lucia"),
    ('MF',"Saint Martin (French part)"),
    ('PM',"Saint Pierre and Miquelon"),
    ('VC',"Saint Vincent and the Grenadines"),
    ('WS',"Samoa"),
    ('SM',"San Marino"),
    ('ST',"Sao Tome and Principe"),
    ('SA',"Saudi Arabia"),
    ('SN',"Senegal"),
    ('RS',"Serbia"),
    ('SC',"Seychelles"),
    ('SL',"Sierra Leone"),
    ('SG',"Singapore"),
    ('SX',"Sint Maarten (Dutch part)"),
    ('SK',"Slovakia"),
    ('SI',"Slovenia"),
    ('SB',"Solomon Islands"),
    ('SO',"Somalia"),
    ('ZA',"South Africa"),
    ('GS',"South Georgia and the South Sandwich Islands"),
    ('SS',"South Sudan"),
    ('ES',"Spain"),
    ('LK',"Sri Lanka"),
    ('SD',"Sudan"),
    ('SR',"Suriname"),
    ('SJ',"Svalbard and Jan Mayen"),
    ('SZ',"Swaziland"),
    ('SE',"Sweden"),
    ('CH',"Switzerland"),
    ('SY',"Syrian Arab Republic"),
    ('TW',"Taiwan, Province of China"),
    ('TJ',"Tajikistan"),
    ('TZ',"Tanzania, United Republic of"),
    ('TH',"Thailand"),
    ('TL',"Timor-Leste"),
    ('TG',"Togo"),
    ('TK',"Tokelau"),
    ('TO',"Tonga"),
    ('TT',"Trinidad and Tobago"),
    ('TN',"Tunisia"),
    ('TR',"Turkey"),
    ('TM',"Turkmenistan"),
    ('TC',"Turks and Caicos Islands"),
    ('TV',"Tuvalu"),
    ('UG',"Uganda"),
    ('UA',"Ukraine"),
    ('AE',"United Arab Emirates"),
    ('GB',"United Kingdom"),
    ('US',"United States"),
    ('UM',"United States Minor Outlying Islands"),
    ('UY',"Uruguay"),
    ('UZ',"Uzbekistan"),
    ('VU',"Vanuatu"),
    ('VE',"Venezuela, Bolivarian Republic of"),
    ('VN',"Viet Nam"),
    ('VG',"Virgin Islands, British"),
    ('VI',"Virgin Islands, U.S."),
    ('WF',"Wallis and Futuna"),
    ('EH',"Western Sahara"),
    ('YE',"Yemen"),
    ('ZM',"Zambia"),
    ('ZW',"Zimbabwe")
)

class UserType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    phone = models.CharField(max_length=50, unique=True)
    fax = models.CharField(max_length=50, unique=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=2, choices = COUNTRY_CHOICES)
    address = models.CharField(max_length=255, default="N/A")
    postcode = models.CharField(max_length=10)
    user_type = models.ForeignKey(UserType, default=0)

    orders = jsonfield.JSONField(default="{}")

    location = PlainLocationField(based_fields=['address'], zoom=7)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class OrderStatus(models.Model):
    status_name = models.CharField(max_length = 255)

    def __str__(self):
        return self.status_name

class OrderPriority(models.Model):
    priority_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.priority_name

class Order(models.Model):
    user = models.ForeignKey(User)
    data = jsonfield.JSONField()
    qrcode = models.FileField(upload_to='qrcode', blank=True)
    status = models.ForeignKey(OrderStatus)
    priority = models.ForeignKey(OrderPriority)
    creationdate = models.DateTimeField(auto_now=True)

    # geo_pickup = PlainLocationField(based_fields=['pick_up_location'], zoom=7)
    # geo_drop = PlainLocationField(based_fields=['drop_location'], zoom=7)

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=0,
        )
        content = {}
        content['id'] = self.id
        # content['content'] = self.data
        content['time'] = unicode(self.creationdate)
        print unicode(json.dumps(content))
        qr.add_data(unicode(json.dumps(content)))
        qr.make(fit=True)

        img = qr.make_image()

        buffer = StringIO.StringIO()
        img.save(buffer)
        filename = 'order-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.len, None)
        self.qrcode.save(filename, filebuffer)

    def __str__(self):
        data = json.loads(self.data)
        info = ''
        try:
            name = data['service']['service']['itemName']
            if name != 'Property':
                raise ValueError('No Property!')
            info = 'Property - '
            for key in data['service']['service'][name]:
                info = info + data['service']['service'][name][key]['value']
        except:
            pass
        try:
            return self.user.userprofile.__str__() + "'s Order  on '" + self.creationdate.strftime("%Y-%m-%d %H:%M:%S")  + ' : ' + info
        except:
            return self.user.__str__() + "'s Order  on '" + self.creationdate.strftime("%Y-%m-%d %H:%M:%S") +' no profile' + ' : ' + info

class OrderAction(models.Model):
    action_name = models.CharField(max_length = 255)

    def __str__(self):
        return self.action_name

class TrackStatus(models.Model):
    status_name = models.CharField(max_length = 255)

    def __str__(self):
        return self.status_name

class Track(models.Model):

    time = models.DateTimeField(auto_now=True)
    from_user = models.ForeignKey(User, related_name='from_user', blank=True, null=True)
    to_user = models.ForeignKey(User, related_name='to_user', blank=True, null=True)
    description = models.CharField(max_length=255)
    order = models.ForeignKey(Order)

    def __str__(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S") + self.order.__str__()
