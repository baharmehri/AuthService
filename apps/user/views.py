from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import CreateUserInputSerializer, CreateUserOutputSerializer, UserOutputSerializer, \
    UserInputUpdateSerializer
from .models import CustomUser

from apps.core.response import CustomResponse
from .services import update_user_info


class UsersRegister(APIView):
    @extend_schema(
        request=CreateUserInputSerializer,
        responses={
            201: "User created successfully.",
            400: "Malformed request or missing required parameters.",
            500: "An unexpected error occurred."
        },
        summary="Create new user",
        description="""
        This route creates a new user with the provided information.

        **Parameters:**
        - `email` (string, required): The email address of the user.
        - `password` (string, required): The password for the user.
        - `is_admin` (boolean, optional): Indicates whether the user is an administrator. Default is `false`.

        **Request Body:**
        This route expects a JSON object containing the following properties:
        - `email` (string, required): The email address of the user.
        - `password` (string, required): The password for the user.
        - `is_admin` (boolean, optional): Indicates whether the user is an administrator. Default is `false`.

        **Response:**
        - 201 Created: The user was created successfully.
        - 400 Bad Request: If the request is malformed or missing required parameters.
        - 500 Internal Server Error: If an unexpected error occurs.
        """
    )
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
            message="User created successfully",
            status=status.HTTP_201_CREATED
        )


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: "User information returned successfully.",
            403: "User does not have the required permission.",
            404: "User with the specified ID not found.",
            500: "An unexpected error occurred."
        },
        summary="Get user information by ID",
        description="""
        This route retrieves information about a specific user based on the provided `id`.

        **Parameters:**
        - `id` (string, required): The unique identifier of the user.

        **Response:**
        - 200 OK: Returns the user's details in JSON format.
        - 403 Forbidden: If the user does not have the required permission.
        - 404 Not Found: If the user with the specified ID doesn't exist.
        - 500 Internal Server Error: If an unexpected error occurs.
        """
    )
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

    @extend_schema(
        request=UserInputUpdateSerializer,
        responses={
            201: "User information updated successfully.",
            403: "User does not have the required permission.",
            404: "User with the specified ID not found.",
            500: "An unexpected error occurred."
        },
        summary="Update user information by ID",
        description="""
        This route updates the information of a specific user based on the provided `id`.

        **Parameters:**
        - `id` (string, required): The unique identifier of the user.

        **Request Body:**
        This route expects a JSON object containing the following properties:
        - `username` (string, optional): The username of the user.
        - `first_name` (string, optional): The first name of the user.
        - `last_name` (string, optional): The last name of the user.

        **Response:**
        - 200 OK: Returns the updated user's details in JSON format.
        - 403 Forbidden: If the user does not have the required permission.
        - 404 Not Found: If the user with the specified ID doesn't exist.
        - 500 Internal Server Error: If an unexpected error occurs.
        """
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

    @extend_schema(
        responses={
            204: "User deleted successfully.",
            403: "User does not have the required permission.",
            404: "User with the specified ID not found.",
            500: "An unexpected error occurred."
        },
        summary="Delete user by ID",
        description="""
        This route deletes a specific user based on the provided `id`.

        **Parameters:**
        - `id` (string, required): The unique identifier of the user.

        **Response:**
        - 204 No Content: User deleted successfully.
        - 403 Forbidden: If the user does not have the required permission.
        - 404 Not Found: If the user with the specified ID doesn't exist.
        - 500 Internal Server Error: If an unexpected error occurs.
        """
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
        return Response("User deleted successfully", status=status.HTTP_204_NO_CONTENT)
