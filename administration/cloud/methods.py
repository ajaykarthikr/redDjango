from administration.models import cloud
from administration.cloud.serializers import (
    addCloudSerializer, cloudSerializer)
from essentials.methods import generateRandom
from redDjango.constants import BUCKET_NAME


def createCloud(u, name):
    if cloud.objects.filter(user=u).exists():
        return None
    cloudDict = {}
    cloudDict['name'] = name
    cloudDict['user'] = u.id
    cloudDict['cloudAddress'] = generateRandom(32)
    cloudDict['bucketName'] = BUCKET_NAME
    serObj = addCloudSerializer(data=cloudDict)
    if not serObj.is_valid():
        return None
    c = serObj.save()
    return cloudSerializer(c).data
