from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateUserInputSerializer, CreateUserOutputSerializer, UserOutputSerializer, \
    UserInputUpdateSerializer
from .models import CustomUser

from apps.core.response import CustomResponse
from apps.core.permissions import IsAdmin
from .services import update_user_info


class UsersRegister(APIView):
    def post(self, request):
        serializers = CreateUserInputSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            user = CustomUser.objects.create_user(email=serializers.validated_data['email'],
                                                  password=serializers.validated_data['password'],
                                                  is_admin=serializers.validated_data.get('is_admin', False)
                                                  )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return CustomResponse.data_response(
            data=CreateUserOutputSerializer(user, context={'request': request}).data,
            message="user created successfully",
            status=status.HTTP_201_CREATED
        )


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.pk != id:
            if not request.user.is_admin:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response("user not found", status=status.HTTP_404_NOT_FOUND)
        return CustomResponse.data_response(
            data=UserOutputSerializer(user, context={'request': request}).data,
            message="User found successfully",
            status=status.HTTP_200_OK
        )

    def put(self, request, id):
        if request.user.pk != id:
            if not request.user.is_admin:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
        try:
            CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response("user not found", status=status.HTTP_404_NOT_FOUND)

        serializer = UserInputUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        try:
            user = update_user_info(
                user=request.user,
                username=serializer.validated_data.get('username'),
                first_name=serializer.validated_data.get('first_name'),
                last_name=serializer.validated_data.get('last_name')
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return CustomResponse.data_response(
            UserOutputSerializer(user, context={'request': request}).data,
            message="user updated successfully",
            status=status.HTTP_200_OK
        )

    def delete(self, request, id):
        if request.user.pk != id:
            if not request.user.is_admin:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response("user not found", status=status.HTTP_404_NOT_FOUND)

        try:
            user.delete()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response("User deleted successfully", status=status.HTTP_200_OK)
