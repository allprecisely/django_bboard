from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_400_BAD_REQUEST

# from django.shortcuts import get_object_or_404

from main import models
from api import serializers


@api_view(['GET'])
def bbs(request):
    bbs = models.Bb.objects.filter(is_active=True)[:10]
    serializer = serializers.BbSerializer(bbs, many=True)
    return Response(serializer.data)


class BbDetailView(RetrieveAPIView):
    queryset = models.Bb.objects.filter(is_active=True)
    serializer_class = serializers.BbDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):
    if request.method == 'POST':
        print(request.data)
        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = models.Comment.objects.filter(is_active=True, bb=pk)
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)


# @api_view(['GET'])
# def detail(request, pk):
#     bb = get_object_or_404(models.Bb, pk=pk)
#     serializer = serializers.BbDetailSerializer(bb)
#     return Response(serializer.data)
