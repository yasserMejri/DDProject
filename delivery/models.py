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

class UserType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, unique=True, validators=[RegexValidator(regex='^\d{10,}$', message='Length has to be longer than 10', code='Invalid number')], default=10000000000000)
    address = models.CharField(max_length=255, default="N/A")
    user_type = models.ForeignKey(UserType, default=0)

    location = PlainLocationField(based_fields=['address'], zoom=7)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class OrderStatus(models.Model):
    status_name = models.CharField(max_length = 255)

    def __str__(self):
        return self.status_name

class OrderPriority(models.Model):
    priority_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.priority_name

class Order(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    pick_up_location = models.CharField(max_length=255)
    drop_location_title = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    qrcode = models.FileField(upload_to='qrcode', blank=True)
    status = models.ForeignKey(OrderStatus)
    priority = models.ForeignKey(OrderPriority)
    creationdate = models.DateTimeField(auto_now=True)
    service = jsonfield.JSONField()

    geo_pickup = PlainLocationField(based_fields=['pick_up_location'], zoom=7)
    geo_drop = PlainLocationField(based_fields=['drop_location'], zoom=7)

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=12,
            border=0,
        )
        qr.add_data(str(self.id)+":")
        qr.add_data(str(self.sender.id)+":")
        qr.add_data(str(self.pick_up_location)+":")
        qr.add_data(str(self.drop_location)+":")
        qr.add_data(str(self.receiver.id)+":")
        qr.add_data(self.creationdate)
        qr.make(fit=True)

        img = qr.make_image()

        buffer = StringIO.StringIO()
        img.save(buffer)
        filename = 'order-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.len, None)
        self.qrcode.save(filename, filebuffer)

    def __str__(self):
        return self.sender.__str__() + ' to ' + self.receiver.__str__()

class Document(models.Model):
    name =models.CharField(max_length = 100)
    description = models.TextField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order)
    unit_price = models.IntegerField()

    def __str__(self):
        return self.name

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
    ordernum = models.IntegerField()
    address1 = models.CharField(max_length=255)
    location1 = models.CharField(max_length=255)
    location2 = models.CharField(max_length=255)
    from_user = models.ForeignKey(User, related_name='from_user', blank=True, null=True)
    to_user = models.ForeignKey(User, related_name='to_user', blank=True, null=True)
    next_user = models.ForeignKey(User, related_name="next_user", blank=True, null=True)
    order = models.ForeignKey(Order)
    status = models.ForeignKey(TrackStatus)
    action = models.ForeignKey(OrderAction)

    def __str__(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S") + self.order.__str__()
