#coding:utf8
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class user_info(models.Model):
    server_name = models.CharField(max_length=1000)
    user_name = models.CharField(max_length=100)
    rent_time = models.DateTimeField(
        'use end time', default=timezone.now)


class RentDB(models.Model):
    d_type = models.CharField(max_length=100)
    d_id = models.CharField(max_length=100)
    d_pic = models.ImageField(upload_to='img')
    p_name = models.CharField(max_length=100)


class TestlinkDB(models.Model):
    # parent_suite_name = models.CharField(max_length=100)
    parent_suite_name = models.ForeignKey(
        'self', blank=True, null=True, related_name='children')
    suite_name = models.CharField(max_length=100)
    suite_detail = models.TextField()
    suite_id = models.CharField(max_length=100)

    def __str__(self):
        return "TestlinkDB"


class TestlinkCase(models.Model):
    case_name = models.CharField(
        max_length=100, default='null', null=True, blank=True)
    case_sum = models.TextField(null=True, blank=True)
    case_step = models.TextField(max_length=4000, null=True, blank=True)
    case_except = models.TextField(null=True, blank=True)
    case_suite = models.ForeignKey('TestlinkDB',
                                   blank=True, null=True,
                                   related_name='children_case')
    internalid = models.CharField(max_length=1000, default='0000')

    def __str__(self):
        return "TestlinkCase"
