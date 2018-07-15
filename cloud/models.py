from __future__ import unicode_literals
from django.db import models
from administration.models import cloud


class file(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    cloud = models.ForeignKey(cloud)
    path = models.CharField(max_length=100)
    isExpired = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    addedTime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    expiryTime = models.DateTimeField(blank=True, null=True)
