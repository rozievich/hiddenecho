from rest_framework import serializers
from .models import CustomUser


class CustomUserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "first_name", "last_name", "email", "bio", "profile_picture", "created_at", "updated_at", "password")
