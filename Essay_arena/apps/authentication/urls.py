from django.urls import path
from .views import (
    ClientRegistration, WriterRegistration, UserLogin
)

urlpatterns = [
    path('users/client/', ClientRegistration.as_view(), name='user_url'),
    path('users/writer/', WriterRegistration.as_view(), name='user_signup'),
    path('users/login/', UserLogin.as_view(), name='user_login'),
]
