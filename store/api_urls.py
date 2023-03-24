from django.urls import path
from .views import ProductDetailView, ProductListView
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    # -----------------API---------------------
    path('product/', ProductListView.as_view()),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('auth/login/', TokenObtainPairView.as_view(),
         name='create-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ------------------------API--------------
]
