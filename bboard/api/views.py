from rest_framework.response import Response
from rest_framework.decorators import api_view

from main import models
from api import serializers


@api_view(['GET'])
def bbs(request):
    bbs = models.Bb.objects.filter(is_active=True)[:10]
    serializer = serializers.BbSerializer(bbs, many=True)
    return Response(serializer.data)
