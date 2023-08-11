from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 2


class ArticleListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination


class ArticleViewSet(viewsets.ViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        context = {
            "request": self.request
        }
        return context

    @action(detail=False, methods=['post'])
    def create_post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def update_article(self, request, pk=None):
        article = Article.objects.get(pk=pk)

        if article.author != request.user:
            return Response(
                {'detail': 'You do not have permission to update this article.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ArticleSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_article(self, request, pk=None):
        article = Article.objects.get(pk=pk)

        if article.author != request.user:
            return Response(
                {'detail': 'You do not have permission to delete this article.'},
                status=status.HTTP_403_FORBIDDEN
            )

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
