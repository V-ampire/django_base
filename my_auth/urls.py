from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'my_auth'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/done/', views.RegisterDoneView.as_view(), name='register_done'),
    path('register/confirm_email/<token>/', views.RegisterConfirmView.as_view(), name='register_confirm'),
    path('register/confirm/done/', views.RegisterConfirmDoneView.as_view(), name='register_confirm_done'),
    path('register/confirm/fail/', views.RegisterConfirmFailView.as_view(), name='register_confirm_fail'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]