from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path

from apps.user.views import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
]
