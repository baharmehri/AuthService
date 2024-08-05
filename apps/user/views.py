from rest_framework.response import Response
from rest_framework import permissions, status, views

from apps.base.views import BaseView
from apps.core.exceptions import NumberInvalid, UserPassInvalid
from apps.user.serializers import LoginSerializer, NumberStatusSerializer, VerifyNumberSerializer


class NumberStatusView(BaseView):

    def post(self, request):
        serializer = NumberStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            number_status = self.user_services.check_number_status(serializer.validated_data.get("number"))
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
            tokens = self.user_services.login_user(
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
        self.user_services.verify_number(number=serializer.validated_data["number"],
                                         code=serializer.validated_data["code"])
        return Response({}, status=status.HTTP_200_OK)
