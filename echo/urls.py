from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserModelViewSet


router = DefaultRouter()
router.register(r"users", CustomUserModelViewSet)


urlpatterns = [
    path("", include(router.urls))
]
