from rest_framework import serializers
from administration.models import User, cloud
from administration.company.methods import checkCompanyAdmin
from administration.cloud.serializers import cloudSerializer


class addUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phoneNumber',
                  'profilePic', 'password')


class userSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phoneNumber', 'profilePic',
                  'dateAdded', 'gender', 'isVerified')


class patchUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'profilePic')


class completeUserSerializer(serializers.ModelSerializer):
    clouds = serializers.SerializerMethodField('getClouds')
    isAdmin = serializers.SerializerMethodField('checkAdmin')

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phoneNumber', 'profilePic',
                        'dateAdded', 'gender', 'isVerified',
                        'isBlocked', 'clouds', 'isAdmin', 'isGoogleLinked',
                        'googleUserId')

    def getClouds(self, u):
        qs = cloud.objects.filter(user=u)
        return cloudSerializer(qs, many=True).data

    def checkAdmin(self, u):
        return checkCompanyAdmin(u)
