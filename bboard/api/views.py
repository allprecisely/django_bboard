from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_400_BAD_REQUEST

from main import models
from api import serializers


@api_view(['GET'])
def articles(request):
    articles = models.Article.objects.filter(is_active=True)[:10]
    serializer = serializers.ArticleSerializer(articles, many=True)
    return Response(serializer.data)


class ArticleDetailView(RetrieveAPIView):
    queryset = models.Article.objects.filter(is_active=True)
    serializer_class = serializers.ArticleDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):
    if request.method == 'POST':
        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = models.Comment.objects.filter(is_active=True, article=pk)
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)
