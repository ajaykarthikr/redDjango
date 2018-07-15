from __future__ import unicode_literals

from django.db import models
from administration.validators import minPhoneLength, genderValidator


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profilePic = models.CharField(max_length=100)
    dateAdded = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='',
        validators=[genderValidator])
    isActive = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)
    isGoogleLinked = models.BooleanField(default=False)
    googleUserId = models.CharField(max_length=100, null=True, blank=True)
    phoneNumber = models.CharField(
        max_length=20, default="", blank=True, validators=[minPhoneLength])
    isBlocked = models.BooleanField(default=False)
    lastActive = models.DateTimeField(null=True, blank=True)


class group(models.Model):
    users = models.ManyToManyField(
        User, through='userGroupInfo', related_name='partOfGroups')

    def nUsers(self):
        return self.users.all().count()


class userGroupInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    dateAdded = models.DateField(auto_now_add=True, blank=True, null=True)
    lastModified = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (("user", "group"),)


class companyAdmin(models.Model):
    user = models.OneToOneField(User)
    dateAdded = models.DateField(auto_now_add=True, blank=True, null=True)
    isActive = models.BooleanField(default=True)


class cloud(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    cloudAddress = models.CharField(max_length=64)
    bucketName = models.CharField(max_length=50)


class subscriptionPlan(models.Model):
    name = models.CharField(max_length=20)
    # storage size is in mb
    storage = models.IntegerField()
    months = models.IntegerField(default=12)


class userSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cloud = models.ForeignKey(cloud, on_delete=models.CASCADE)
    plan = models.ForeignKey(subscriptionPlan, on_delete=models.CASCADE)
    startDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    endDate = models.DateTimeField(blank=True, null=True)


class fileType(models.Model):
    name = models.CharField(max_length=20)
    ext = models.CharField(max_length=10)
