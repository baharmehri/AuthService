from rest_framework.response import Response
from rest_framework import status

from apps.base.views import BaseView
from apps.core.exceptions import NumberInvalid, UserPassInvalid, OTPInvalid
from apps.core.permissions import IsAuthenticatedToSetPassword, IsAuthenticatedUser
from apps.user.serializers import LoginSerializer, NumberStatusSerializer, VerifyNumberSerializer, \
    SetPasswordSerializer, UserProfileSerializer


class NumberStatusView(BaseView):

    def post(self, request):
        serializer = NumberStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            number_status = self.user_service.check_number_status(serializer.validated_data.get("number"))
        except Exception:
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = {
            "number": serializer.validated_data.get("number"),
            "status": number_status
        }
        if number_status is False:
            data.update({"message": "otp sent"})
        return Response(data, status=status.HTTP_200_OK)


class LoginView(BaseView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            tokens = self.user_service.login_user(
                serializer.validated_data.get("number"),
                serializer.validated_data.get("password")
            )
        except NumberInvalid as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        except UserPassInvalid as e:
            return Response({"error": e.message}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(tokens, status=status.HTTP_200_OK)


class VerifyNumberView(BaseView):
    def post(self, request):
        serializer = VerifyNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            tokens = self.user_service.verify_number(number=serializer.validated_data["number"],
                                                     code=serializer.validated_data["code"])
        except OTPInvalid as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(tokens, status=status.HTTP_200_OK)


class NewPasswordView(BaseView):
    permission_classes = [IsAuthenticatedToSetPassword]

    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.user_service.set_password_for_new_user(request.user, serializer.validated_data.get("password"))
        except Exception:
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Password has been set successfully."}, status=status.HTTP_200_OK)


class UpdateProfileView(BaseView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            profile = serializer.save()
            return Response(UserProfileSerializer(profile).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
