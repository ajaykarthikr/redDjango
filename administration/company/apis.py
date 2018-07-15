from rest_framework.response import Response
from rest_framework.decorators import api_view
from login.methods import loginAPI
from administration.models import (
    User, companyAdmin, subscriptionPlan,
    fileType)
from administration.company.serializers import (
    subscriptionPlanSerializer, companyAdminSerializer,
    fileTypeSerializer)
from administration.company.methods import (
    checkCompanyAdmin, addCompanyAdmin, deleteCompanyAdmin)
from essentials.methods import (
    errorResponse, checkObject,
    getPaginatedData)


@api_view(['GET', 'POST'])
@loginAPI(loginRequired=True)
def adminAPI(request):
    user = request.user
    getParams = request.GET
    inputDict = request.data
    if not checkCompanyAdmin(user):
        return errorResponse(403)
    if request.method == 'GET':
        queryset = companyAdmin.objects.all()
        return Response(getPaginatedData(queryset, companyAdminSerializer,
                                         getParams, {'user': user}))
    elif request.method == 'POST':
        if 'type' in getParams:
            typ = getParams['type']
            if typ == 'add':
                if 'userId' not in inputDict:
                    return errorResponse(406)
                uid = inputDict['userId']
                newAdmin = checkObject(User, id=uid)
                if checkCompanyAdmin(newAdmin):
                    return errorResponse(406, "Already Added")
                addCompanyAdmin(newAdmin)
                return Response()
            elif typ == 'delete':
                if 'userId' not in inputDict:
                    return errorResponse(406)
                uid = inputDict['userId']
                admin = checkObject(User, id=uid)
                deleteCompanyAdmin(admin)
                return Response()
    return errorResponse(400)


@api_view(['GET', 'PUT'])
@loginAPI(loginRequired=True)
def subscriptionAPI(request):
    user = request.user
    getParams = request.GET
    inputDict = request.data
    if not checkCompanyAdmin(user):
        return errorResponse(403)
    if request.method == 'GET':
        queryset = subscriptionPlan.objects.all()
        return Response(getPaginatedData(queryset,
                                         subscriptionPlanSerializer,
                                         getParams, {'user': user}))
    elif request.method == 'PUT':
        serObj = subscriptionPlanSerializer(data=inputDict)
        if not serObj.is_valid():
            errStr = 'Invalid data'
            return errorResponse(406, errStr)
        sPlan = serObj.save()
        return Response({'result':
                         {'subscriptionPlan':
                          subscriptionPlanSerializer(sPlan).data}})
    return errorResponse(400)


@api_view(['GET', 'PUT'])
@loginAPI(loginRequired=True)
def fileTypeAPI(request):
    user = request.user
    getParams = request.GET
    inputDict = request.data
    if not checkCompanyAdmin(user):
        return errorResponse(403)
    if request.method == 'GET':
        queryset = fileType.objects.all()
        return Response(getPaginatedData(queryset,
                                         fileTypeSerializer,
                                         getParams, {'user': user}))
    elif request.method == 'PUT':
        serObj = fileTypeSerializer(data=inputDict)
        if not serObj.is_valid():
            errStr = 'Invalid data'
            return errorResponse(406, errStr)
        fType = serObj.save()
        return Response({'result':
                         {'fileType':
                          fileTypeSerializer(fType).data}})
