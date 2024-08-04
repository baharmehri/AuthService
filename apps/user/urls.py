from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path

from apps.user.views import NumberStatusView

urlpatterns = [
    path('check-number', NumberStatusView.as_view(), name='check-number'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
]
