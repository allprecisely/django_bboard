from rest_framework import serializers

from main import models


class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bb
        fields = ('id', 'title', 'content', 'price', 'created_at')
