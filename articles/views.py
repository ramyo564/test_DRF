from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class CustomPagination(PageNumberPagination):
    """
    사용자 정의 Pagination class 입니다.
    페이지당 게시글 수를 2개로 설정합니다.
    """
    page_size = 2


class ArticleListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    게시글 목록을 조회하는 ViewSet class 입니다.

        매개변수: (게시글, 혹은 페이지 넘버)
        - id (int): 게시글 id, 페이지 넘버

        반환값:
        - 생성된 게시글 정보

        오류:
        - 404 Bad Not Found: 게시글이 존재하지 않는 경우.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """
        게시글을 조회하는 데 사용할 시리얼라이저 클래스를 반환합니다.

            Returns:
                CustomArticleSerializer: 'author' 필드를 추가한 시리얼라이저 클래스입니다.

        """
        class CustomArticleSerializer(serializers.ModelSerializer):
            author = serializers.CharField(source='author.email', read_only=True)

            class Meta:
                model = Article
                fields = '__all__'

        return CustomArticleSerializer


class ArticleViewSet(viewsets.ViewSet):
    """
    게시글을 생성, 수정, 삭제하는 ViewSet class 입니다.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        """
        시리얼라이저 인스턴스를 생성하여 반환합니다.
        """
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        """
        시리얼라이저에 전달할 컨텍스트 정보를 반환합니다.
        """

        context = {
            "request": self.request
        }
        return context

    @action(detail=False, methods=['post'])
    def create_article(self, request):
        """
        새 게시글을 생성합니다.

            매개변수:
                - title (str): 게시글 제목
                - content (str): 게시글 내용

            반환값:
                - 생성된 게시글 정보

            오류:
                - 400 Bad Request: 제공된 데이터가 유효하지 않은 경우.
                - 401 Unauthorized: 로그인 하지 않았을 경우
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def update_article(self, request, pk=None):
        """
        기존 게시글을 수정합니다.

            매개변수:
                - pk (int): 수정할 게시글의 고유 ID
                - title (str): 수정할 게시글 제목
                - content (str): 수정할 게시글 내용

            반환값:
                - 수정된 게시글 정보

            오류:
                - 400 Bad Request: 제공된 데이터가 유효하지 않은 경우.
                - 401 Unauthorized: 로그인 하지 않았을 경우
                - 403 Forbidden: 게시글 작성자가 아닌 사용자가 수정을 시도한 경우.
                - 404 Not Found: 게시글이 존재하지 않는 경우.
        """
        article = get_object_or_404(Article, pk=pk)

        if article.author != request.user:
            return Response(
                {'detail': '해당 글을 업데이트할 권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ArticleSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_article(self, request, pk=None):
        """
        게시글을 삭제합니다.

            매개변수:
                - pk (int): 삭제할 게시글의 고유 ID

            반환값:
                - 삭제 성공 시 204 No Content 반환

            오류:
                - 403 Forbidden: 게시글 작성자가 아닌 사용자가 삭제를 시도한 경우.
                - 404 Not Found: 게시글이 존재하지 않는 경우.
        """
        article = get_object_or_404(Article, pk=pk)

        if article.author != request.user:
            return Response(
                {'detail': '해당 글을 삭제할 권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        article.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
