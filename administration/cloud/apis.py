from rest_framework.response import Response
from rest_framework.decorators import api_view
from login.methods import loginAPI
from essentials.methods import checkObject, errorResponse
from administration.models import cloud
from administration.cloud.serializers import cloudSerializer
from administration.cloud.methods import createCloud


@api_view(['GET', 'POST'])
@loginAPI(loginRequired=True)
def cloudDetailAPI(request, cloudId):
    user = request.user
    # getParams = request.GET
    # inputDict = request.data
    c = checkObject(cloud, id=cloudId)
    if c.user != user:
        return errorResponse(403)
    if request.method == 'GET':
        resp = cloudSerializer(c).data
        return Response({'result': resp})
    return errorResponse(400)


@api_view(['GET', 'POST', 'PUT'])
@loginAPI(loginRequired=True)
def cloudListAPI(request):
    user = request.user
    getParams = request.GET
    inputDict = request.data
    if request.method == 'GET':
        if 'type' in getParams:
            typ = getParams['type']
            if typ == 'all':
                queryset = cloud.objects.filter(user=user)
                resp = cloudSerializer(queryset, many=True).data
                return Response({'result': resp})
    elif request.method == 'PUT':
        if 'name' not in inputDict:
            return errorResponse(406)
        cloudData = createCloud(user, inputDict['name'])
        if cloudData is None:
            return errorResponse(406, "Error Occured!")
        return Response({'result': cloudData})
    return errorResponse(400)
