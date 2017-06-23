"""ddproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from delivery import views as d_views
from service import views as s_views
from postman import views as pm_views
from pcenter import views as pc_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', d_views.index, name="home"), 
    url(r'^login/$', d_views.d_login, name="login"), 
    url(r'^logout/$', d_views.d_logout, name="logout"), 
    url(r'^register/$', d_views.register, name="register"), 
    url(r'^new_order/$', d_views.new_order, name="new_order"), 
    url(r'^order_view/(?P<pk>\d{0,50})/$', d_views.order_review, name="order_review"), 
    url(r'^order_list/$', d_views.order_list, name="order_list"), 
    url(r'^order_confirm/(?P<oid>\d{0,50})/(?P<uid>\d{0,50})/$', d_views.order_confirm, name="order_confirm"), 
    url(r'^order_track/(?P<oid>\d{0,50})/$', d_views.order_track, name="order_track"), 
    url(r'^service_autocomplete/$', s_views.service_autocomplete, name="service_autocomplete"), 

    url(r'^postman/add_order/$', pm_views.register_order, name="postman_register_order"), 
    url(r'^postman/order_list/$', pm_views.order_list, name="postman_order_list"), 
    url(r'^postman/order/next/$', pm_views.order_next, name="postman_order_next"), 
    url(r'^postman/order/next_bulk/$', pm_views.order_next_bulk, name="postman_order_next_bulk"), 
    url(r'^postman/order/confirm/$', pm_views.confirm_order, name="postman_order_confirm"), 
    url(r'^postman/order/confirm_bulk/$', pm_views.confirm_order_bulk, name="postman_order_confirm_bulk"), 

    url(r'^pcenter/order_list/$', pc_views.order_list, name="pcenter_order_list"), 
    url(r'^pcenter/add_order/$', pc_views.register_order, name="pcenter_register_order"), 
    url(r'^pcenter/order/next/$', pc_views.order_next, name="pcenter_order_next"), 
    url(r'^pcenter/order/next_bulk/$', pc_views.order_next_bulk, name="pcenter_order_next_bulk"), 
    url(r'^pcenter/order/confirm/$', pc_views.confirm_order, name="pcenter_order_confirm"), 
    url(r'^pcenter/order/confirm_bulk/$', pc_views.confirm_order_bulk, name="pcenter_order_confirm_bulk")

]
