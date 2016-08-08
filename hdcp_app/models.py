from django.db import models

# Create your models here.
class test_table(models.Model):
    user = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)

class test_table2(models.Model):
    user = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)