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
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    @action(detail=False, methods=['POST'], url_path='register')
    def register(self, request):
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
