from __future__ import unicode_literals

from django.db import models
from administration.models import User


class session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    authToken = models.CharField(max_length=128, unique=True)
    isExpired = models.BooleanField(default=False)
    createdTime = models.DateTimeField(blank=True, null=True)
