from rest_framework import serializers

from main import models


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ('id', 'title', 'content', 'created_at')


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ('id', 'title', 'content', 'created_at', 'image')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('article', 'author', 'content', 'created_at')
