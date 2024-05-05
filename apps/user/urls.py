from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

from apps.user.views import UsersRegister, UserView, VerifyUserView

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('', UsersRegister.as_view(), name='users-register'),
    path('verify/<str:token>', VerifyUserView.as_view(), name='verify_user'),
    path('<int:id>', UserView.as_view(), name='users-view'),
]
