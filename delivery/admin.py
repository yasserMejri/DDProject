# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from delivery import models

class ProfileInline(admin.StackedInline):
    model = models.UserProfile

# UserAdmin.list_display += ('get_full_name',)
# UserAdmin.list_filter += ('userprofile',)
# UserAdmin.fieldsets += ('userprofile',)

UserAdmin.inlines = [ProfileInline]

# Register your models here.


# admin.site.register(models.OrderStatus)

# admin.site.register(models.OrderPriority)

# admin.site.register(models.Order)


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
