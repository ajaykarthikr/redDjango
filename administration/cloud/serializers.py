from rest_framework import serializers
from administration.models import cloud


class addCloudSerializer(serializers.ModelSerializer):

    class Meta:
        model = cloud
        fields = ('user', 'name', 'cloudAddress', 'bucketName')


class cloudSerializer(serializers.ModelSerializer):

    class Meta:
        model = cloud
        fields = ('id', 'user', 'name', 'cloudAddress', 'bucketName')
