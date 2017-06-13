from django import forms

from delivery import models as d_models
from service import models as s_models

class OrderRegisterForm(forms.Form):
	qrcode = forms.CharField(max_length==255)
	fromWho = forms.IntegerField()
