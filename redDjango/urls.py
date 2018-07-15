from django.conf.urls import url
from login.apis import (userLoginAPI, signupAPI,
                        googleLoginAPI, googleSignupAPI)
from administration.company.apis import (
    adminAPI, subscriptionAPI, fileTypeAPI)
from administration.cloud.apis import (cloudListAPI, cloudDetailAPI)
from essentials.apis import supportedFileTypeAPI

urlpatterns = [
    url(r'^api/v1/login/$', userLoginAPI),
    url(r'^api/v1/login/signup/$', signupAPI),
    url(r'^api/v1/login/signup/google/$', googleSignupAPI),
    url(r'^api/v1/login/gooogle/$', googleLoginAPI),
    #  url(r'^v1/node_api/$', testMessage),
]

urlpatterns += [
    url(r'api/v1/admin/company/admin/$', adminAPI),
    url(r'api/v1/admin/company/subscription/$', subscriptionAPI),
    url(r'api/v1/admin/company/filetype/$', fileTypeAPI),
]

urlpatterns += [
    url(r'api/v1/admin/cloud/$', cloudListAPI),
    url(r'api/v1/admin/cloud/(?P<cloudId>\d+)/$', cloudDetailAPI),
]

urlpatterns += [
    url(r'api/v1/essentials/filetype/$', supportedFileTypeAPI),
]
