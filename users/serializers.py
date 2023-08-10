from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("이메일 주소에 @가 포함되어야 합니다.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8자리 이상으로 만들어주세요")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
