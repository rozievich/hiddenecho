from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser, Follow
from .serializers import CustomUserModelSerializer, FollowModelSerializer
from .permissions import IsVerifiedUser


class CustomUserModelViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserModelSerializer
    permission_classes = (IsVerifiedUser, )
    parser_classes = (MultiPartParser, )


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            user = CustomUser.objects.get(verification_token=token)
            user.is_verified = True
            user.verification_token = ''
            user.save()
            return Response({'message': 'Email verified!'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)


class FollowModelViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowModelSerializer
    permission_classes = (IsVerifiedUser, )
    parser_classes = (MultiPartParser, )
