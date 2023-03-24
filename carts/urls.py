from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name= 'cart'),
    path('add_cart/<int:product_id>/', views.add_to_cart, name= 'add_to_cart'),
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name= 'decrease_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name= 'remove_cart_item'),
    path('checkout/', views.checkout, name= 'checkout'),


    path('wish', views.wish, name= 'wish'),
    path('add_wishlist/<int:product_id>/', views.add_wishlist, name= 'add_wishlist'),



]
