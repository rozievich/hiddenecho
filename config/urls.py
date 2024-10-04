from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="Hidden Echo API",
      default_version='v1.0',
      description="Hidden Echo — Write, forget, listen to the voices of others",
      terms_of_service="https://www.github.com/rozievich/hiddenecho/",
      contact=openapi.Contact(email="oybekrozievich@gmail.com")
   ),
   public=False,
   permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('echo.urls')),
    # Swagger URL'lari
    path('swdoc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # JWT token olish va yangilash
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
