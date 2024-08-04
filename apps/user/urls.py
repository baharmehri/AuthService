from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path

from apps.user.views import NumberStatusView, LoginView

urlpatterns = [
    path('check-number', NumberStatusView.as_view(), name='check-number'),
    path('login', LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
]
