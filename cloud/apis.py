from rest_framework.response import Response
from rest_framework.decorators import api_view
from login.methods import loginAPI
from essentials.methods import (
    checkObject, errorResponse)


@api_view(['GET'])
@loginAPI(loginRequired=True)
def cloudAPI(request):
    return errorResponse(400)
