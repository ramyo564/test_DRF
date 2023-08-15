from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import UserRegistrationSerializer
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer


User = get_user_model()


class UserViewSet(ViewSet):
    """
    사용자 등록 및 로그인에 대한 API 엔드포인트입니다.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    @action(detail=False, methods=['POST'], url_path='register')
    def register(self, request):
        """
        새 사용자를 등록합니다.

            매개변수:
                - email (str): 사용자의 이메일.
                - password (str): 사용자의 비밀번호.

            반환값:
                - message: 사용자 등록이 성공한 경우의 메시지.

            오류:
                - 400 Bad Request: 제공된 데이터가 유효하지 않은 경우.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get("password")
            hashed_password = make_password(password)
            User.objects.create(
                email=serializer.validated_data.get("email"),
                password=hashed_password
            )
            return Response(
                {
                    "message": "유저 등록 성공",
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        사용자를 로그인하고 액세스 및 리프레시 토큰을 생성합니다.

            매개변수:
                - email (str): 사용자의 이메일.
                - password (str): 사용자의 비밀번호.

            반환값:
                - access_token: 인증을 위한 JWT 액세스 토큰.
                - refresh_token: 새로운 액세스 토큰을 얻기 위한 리프레시 토큰.
                - message: 로그인이 성공한 경우의 메시지.

            오류:
                - 400 Bad Request: 제공된 데이터가 유효하지 않은 경우.
                - 401 Unauthorized: 이메일 또는 비밀번호가 유효하지 않은 경우.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response(
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "message": "로그인 성공",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "이메일 혹은 비밀번호가 유효하지 않습니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
