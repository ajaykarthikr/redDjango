from rest_framework.response import Response
from rest_framework.decorators import api_view
# from login.methods import loginAPI
from administration.models import fileType
from administration.company.serializers import fileTypeSerializer
from essentials.methods import getPaginatedData


@api_view(['GET'])
def supportedFileTypeAPI(request):
    getParams = request.GET
    if request.method == 'GET':
        queryset = fileType.objects.all()
    return Response(getPaginatedData(queryset,
                                     fileTypeSerializer,
                                     getParams))
