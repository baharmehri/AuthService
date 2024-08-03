from django.contrib.auth import authenticate
from rest_framework.views import APIView

from apps.user.serializers import LoginSerializer


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer.InputLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, number=serializer.validated_data["number"],
                            password=serializer.validated_data["password"])
