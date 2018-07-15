from rest_framework.response import Response
from rest_framework.decorators import api_view
from google.oauth2 import id_token
from google.auth.transport import requests

from administration.models import User
from administration.user.serializers import (
    addUserSerializer, userSerializer,
    patchUserSerializer, completeUserSerializer)
from administration.cloud.serializers import cloudSerializer
from administration.cloud.methods import createCloud
from essentials.methods import errorResponse, encryptPassword, checkPassword
from login.methods import newSession
from redDjango.constants import CLIENT_ID
from essentials.methods import generateRandom, checkObject


@api_view(['POST'])
def userLoginAPI(request):
    inputDict = request.data
    if 'email' in inputDict and 'password' in inputDict:
        if not User.objects.filter(email=inputDict['email']).exists():
            return errorResponse(404)
        user = User.objects.get(email=inputDict['email'])
        if not checkPassword(user, inputDict['password']):
            return errorResponse(401)
        if not user.isVerified:
            return errorResponse(403, "Email not verified")
        if user.isBlocked:
            return errorResponse(403, "User is blocked")
        s = newSession(user)
        authToken = s.authToken
        resp = {"userAuth": authToken,
                "user": completeUserSerializer(user).data}
        return Response(resp)
    else:
        return errorResponse(406, "Email and Password not valid")
    return errorResponse(400)


@api_view(['POST'])
def signupAPI(request):
    inputDict = request.data
    if request.method == "POST":
        userDict = inputDict
        if 'password' not in userDict:
            return errorResponse(406)
        if len(userDict['password']) < 7:
            return errorResponse(406,
                                 "Password should be more than 7 characters")
        userDict['password'] = encryptPassword(userDict['password'])
        print userDict['password']
        if 'name' not in userDict:
            return errorResponse(406)
        dP = "https://www.shareicon.net/data/128x128/2016/05/29/772558_user_512x512.png"
        if 'profilePic' not in userDict:
            userDict['profilePic'] = dP
        if userDict['profilePic'] == "":
            userDict['profilePic'] = dP
        serObj = addUserSerializer(data=userDict)
        if not serObj.is_valid():
            errStr = 'Invalid data'
            errs = serObj.errors
            print serObj.errors
            if 'email' in errs:
                errStr = errs['email'][0]
            return errorResponse(406, errStr)
        user = serObj.save()
        cName = user.name + " Cloud"
        c = createCloud(user, cName)
        if c is None:
            resp = {"user": userSerializer(user).data}
        resp = {"user": userSerializer(
            user).data, 'cloud': c}
        return Response(resp)
    return errorResponse(400)


@api_view(['POST'])
def googleLoginAPI(request):
    inputDict = request.data
    if request.method == 'POST':
        if "token" not in inputDict:
            return errorResponse(406)
        token = inputDict['token']
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            if not idinfo['email_verified']:
                return errorResponse(406, "Email not verified")
            userDict = {}
            userDict['name'] = idinfo['name']
            userDict['profilePic'] = idinfo['picture']
            user = checkObject(User, email=idinfo['email'])
            serObj = patchUserSerializer(user, data=userDict, partial=True)
            if not serObj.is_valid():
                print serObj.errors
            else:
                user = serObj.save()
            s = newSession(user)
            authToken = s.authToken
            resp = {"userAuth": authToken, "user": completeUserSerializer(
                user).data}
            return Response(resp)
        except ValueError:
            # Invalid token
            return errorResponse(406, "Invalid Token Id")
    return errorResponse(400)


@api_view(['POST'])
def googleSignupAPI(request):
    inputDict = request.data
    if request.method == "POST":
        if "token" not in inputDict:
            return errorResponse(406)
        token = inputDict['token']
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), CLIENT_ID)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            if not idinfo['email_verified']:
                return errorResponse(406, "Email not verified")
            userDict = {}
            userDict['name'] = idinfo['name']
            userDict['email'] = idinfo['email']
            userDict['password'] = generateRandom(32)
            userDict['profilePic'] = idinfo['picture']
            serObj = addUserSerializer(data=userDict)
            if not serObj.is_valid():
                errStr = 'Invalid data'
                errs = serObj.errors
                print serObj.errors
                if 'email' in errs:
                    errStr = errs['email'][0]
                return errorResponse(406, errStr)
            user = serObj.save()
            user.isVerified = True
            user.save()
            s = newSession(user)
            authToken = s.authToken
            cName = user.name + " Cloud"
            c = createCloud(user, cName)
            resp = {"userAuth": authToken, "user": userSerializer(
                user).data, 'cloud': cloudSerializer(c).data}
            return Response(resp)
        except ValueError:
            # Invalid token
            return errorResponse(406, "Invalid Token Id")
    return errorResponse(400)
