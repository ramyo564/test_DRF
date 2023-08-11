from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.email')

    class Meta:
        model = Article
        fields = '__all__'
