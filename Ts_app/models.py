from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class user_info(models.Model):
    server_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    #rent_time = models.ChoiceField(label=(u"HostName"),required=True, choices=host_name_choice)
    #rent_time = models.CharField(max_length=100)
    rent_time = models.DateTimeField('use end time',default = timezone.now)
class RentDB(models.Model):
    d_type = models.CharField(max_length=100)
    d_id = models.CharField(max_length=100)
    #d_id = models.CharField(max_length=100)
    d_pic = models.ImageField(upload_to='img')
    #d_pic = models.CharField(max_length=100)
    p_name = models.CharField(max_length=100)