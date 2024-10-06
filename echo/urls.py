from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserModelViewSet, VerifyEmailView, FollowModelViewSet


router = DefaultRouter()
router.register(r"users", CustomUserModelViewSet)
router.register(r"follow", FollowModelViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name="verify_email")
]
