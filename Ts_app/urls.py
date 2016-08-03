# coding:utf8
'''
Created on 2016年8月3日

@author: zhangq
'''

from django.conf.urls import url
from Ts_app import views
urlpatterns = [
    url(r'^ts_app/$', views.indexview),
    url(r'^ajax_radio/', views.radioview),
    url(r'^equipment/$', views.rentview),
    url(r'^ajax_list/', views.ajaxview),
    url(r'^ajax_dic/', views.ajaxdicview),
    ]
