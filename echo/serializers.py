from rest_framework import serializers
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from .models import CustomUser, Follow
from config.settings import MAIN_HOST


class CustomUserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "first_name", "last_name", "email", "bio", "profile_picture", "created_at", "updated_at", "is_verified", "password")

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            bio=validated_data.get('bio'),
            profile_picture=validated_data.get('profile_picture')
        )
        user.set_password(validated_data['password'])
        self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        token = get_random_string(length=32)
        user.verification_token = token
        user.save()

        verification_link = f"{MAIN_HOST}/api/verify-email/{token}/"

        send_mail(
            'Tasdiqlash Emaili',
            f'Sizning hisobingizni tasdiqlash uchun quyidagi havolaga bosing: {verification_link}',
            'your_email@example.com',
            [user.email],
            fail_silently=False,
        )


class FollowModelSerializer(serializers.ModelSerializer):
    follower = serializers.HiddenField(default=serializers.CurrentUserDefault())
    follower_data = CustomUserModelSerializer(source='follower', read_only=True)
    following = CustomUserModelSerializer()

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'follower_data', 'following', 'created_at')

    def validate(self, attrs):
        follower = self.context['request'].user
        following = attrs.get('following')

        # Tekshirish: Follower foydalanuvchi tasdiqlanganmi?
        if not follower.is_verified:
            raise serializers.ValidationError("User is not verified. Please verify your account.")

        # Tekshirish: Following foydalanuvchi tasdiqlanganmi?
        if not following.is_verified:
            raise serializers.ValidationError("The user you are trying to follow is not verified.")

        # Tekshirish: O'zini o'zi follow qilmasligi uchun
        if follower == following:
            raise serializers.ValidationError("A user cannot follow themselves.")
        
        return attrs
