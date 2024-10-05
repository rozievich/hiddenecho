from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import CustomUser
from .serializers import CustomUserModelSerializer
from .permissions import IsOwnerPermission, IsAdminPermission


class CustomUserModelViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserModelSerializer
    permission_classes = [IsAdminUser]
    parser_classes = (IsAuthenticated, IsAdminUser)


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            user = CustomUser.objects.get(verification_token=token)
            user.is_verified = True
            user.verification_token = ''
            user.save()
            return Response({'message': 'Email tasdiqlandi!'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Noto‘g‘ri token!'}, status=status.HTTP_400_BAD_REQUEST)
