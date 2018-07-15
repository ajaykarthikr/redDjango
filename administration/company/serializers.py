from rest_framework import serializers
from administration.models import (
    companyAdmin, subscriptionPlan, fileType)
from administration.user.serializers import userSerializer


class companyAdminSerializer(serializers.ModelSerializer):
    user = userSerializer()

    class Meta:
        model = companyAdmin
        fields = ('user', 'id', 'isActive', 'dateAdded')


class subscriptionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = subscriptionPlan
        fields = ('name', 'storage')


class fileTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = fileType
        fields = ('name', 'ext')
