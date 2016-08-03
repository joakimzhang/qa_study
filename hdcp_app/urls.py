# coding:utf8
'''
Created on 2016年8月3日

@author: zhangq
'''
from django.conf.urls import url
from hdcp_app import views
urlpatterns = [
    url('^test/', views.test),
    ]
