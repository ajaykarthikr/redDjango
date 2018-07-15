from django.http import JsonResponse, Http404
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
import datetime
import random
import string
from administration.models import User
from redDjango.constants import (DEFAULT_API_PAGE_SIZE, MAX_API_PAGE_SIZE)


def errorResponse(statusCode=400, displayError="", addData={}):
    errorDict = {'error': {'error': '', 'displayError': displayError}}
    errorText = ""
    if statusCode == 401:
        errorText = "Unauthorized"
    elif statusCode == 403:
        errorText = "Forbidden"
    elif statusCode == 404:
        errorText = "Not Found"
    elif statusCode == 405:
        errorText = "Method Not Allowed"
    else:
        errorText = "Not Acceptable"
    errorDict['error']['error'] = errorText
    return JsonResponse(errorDict, status=statusCode)


def checkPassword(user, password):
    return check_password(password, user.password)


def checkFingerprint(device, deviceFingerprint):
    return check_password(deviceFingerprint, device.deviceFingerprint)


def encryptPassword(password):
    return make_password(password)


def getCurrentTime():
    return datetime.datetime.now()


def generateRandom(length):
    return ''.join([random.choice(
        string.ascii_letters + string.digits) for n in xrange(length)])


def checkObject(model, **args):
    try:
        return get_object_or_404(model, **args)
    except ValueError:
        raise Http404
    except model.MultipleObjectsReturned:
        raise Http404


def checkUserOject(user):
    try:
        User.objects.get(email=user.email)
        return True
    except Exception:
        return False


def getObjectResponse(obj, serializer, contextDict={}):
    return {'result': serializer(obj, context=contextDict).data}


def getPaginatedData(queryset, serializer, getParams, contextDict={},
                     pageSize=DEFAULT_API_PAGE_SIZE):
    if 'pageSize' in getParams:
        try:
            ps = int(getParams['pageSize'])
            if ps > 1:
                pageSize = ps
            if ps > MAX_API_PAGE_SIZE:
                pageSize = MAX_API_PAGE_SIZE
        except ValueError:
            pass
    paginatorObj = Paginator(queryset, pageSize)
    page = 1
    npages = paginatorObj.num_pages
    nobjects = paginatorObj.count
    objects = []
    hasNext = False
    if 'page' in getParams:
        try:
            page = int(getParams['page'])
            if page < 1:
                page = 1
        except ValueError:
            page = 1
    # integer page at this point min 1
    try:
        pageObj = paginatorObj.page(page)
        hasNext = pageObj.has_next()
        objects = pageObj.object_list
    except EmptyPage:
        objects = []
        hasNext = False
    return {'result': serializer(objects, many=True, context=contextDict).data,
            'p': {'nPages': npages, 'nObjects': nobjects, 'pageSize': pageSize,
                  'page': page, 'hasNext': hasNext}}
