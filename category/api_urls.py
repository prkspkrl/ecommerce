from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .views import *
from . import views

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)

from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('category-filter/', CategoryList.as_view(), name='category-filter'),
    # path('category-crud/<int:pk>/', CRUDViewSet.as_view(), name='product-crud'),

    path('auth/login/', TokenObtainPairView.as_view(), name='create-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]