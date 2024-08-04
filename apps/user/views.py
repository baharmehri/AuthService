from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, views
from apps.user.serializers import LoginSerializer, NumberStatusSerializer
from apps.services.user_services import UserServices


class NumberStatusView(APIView):

    def post(self, request):
        serializer = NumberStatusSerializer.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        number_status = UserServices().check_number_status(serializer.validated_data.get("number"))
        data = {
            "number": serializer.validated_data.get("number"),
            "status": number_status
        }
        if number_status is False:
            data.update({"message": "otp sent"})
        return Response(data, status=status.HTTP_200_OK)
