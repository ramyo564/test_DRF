from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import UserRegistrationSerializer
from .models import CustomUser
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password


class UserRegistrationViewSet(ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get("password")
            hashed_password = make_password(password)
            serializer.validated_data["password"] = hashed_password
            serializer.save()  # Save the user instance
            return Response(
                {
                    "message": "User registered successfully"
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
