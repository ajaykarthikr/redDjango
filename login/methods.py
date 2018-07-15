from login.models import session
from essentials.methods import (errorResponse, generateRandom,
                                getCurrentTime, checkObject)


def loginAPI(loginRequired=False, function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            request.user = None
            headers = request.META
            (typ, authToken) = getAuthToken(headers)
            if authToken:
                if not session.objects.filter(authToken=authToken).exists():
                    return authInvalidResponse()
                s = session.objects.get(authToken=authToken)
                if not checkAuthValid(authToken, s):
                    return authInvalidResponse()
                request.user = s.user
                return view_func(request, *args, **kwargs)
            else:
                if loginRequired:
                    return authInvalidResponse()
            return view_func(request, *args, **kwargs)
        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__
        return _view
    if function:
        return _dec(function)
    return _dec


def checkAuthValid(authToken, s):
    return True


def getAuthToken(headers):
    if 'HTTP_AUTHORIZATION' in headers:
        try:
            var = headers['HTTP_AUTHORIZATION'].split('=')
            if len(var) == 2:
                typ = var[0]
                auth = var[1]
                if typ == 'userAuth' and auth:
                    return 'user', auth
                elif typ == 'deiveAuth' and auth:
                    return 'device', auth
        except Exception:
            return None, None
    return None, None


def authExpiredReponse():
    return errorResponse(401, "Auth Expired")


def authInvalidResponse():
    return errorResponse(401, "Auth Invalid")


def newSession(user):
    authToken = generateRandom(128)
    s = session.objects.create(
        user=user, authToken=authToken, createdTime=getCurrentTime())
    return s


def invalidateAllSessions(user):
    pass
