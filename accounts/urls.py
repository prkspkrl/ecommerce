from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name= 'register'),
    path('login', views.login, name= 'login'),
    path('logout', views.logout, name= 'logout'),
    path('dashboard/', views.dashboard, name= 'dashboardurl'),
    path('', views.dashboard, name= 'dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'), #register ko reset validation
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name= 'resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name= 'resetPassword'),


    path('my_order/', views.my_order, name= 'my_order'),
    path('edit_profile/', views.edit_profile, name= 'edit_profile'),
    path('change_password_dashboard/', views.change_password_dashboard, name= 'change_password_dash'),





]