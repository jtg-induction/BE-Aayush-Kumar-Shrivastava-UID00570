from django.contrib.auth import authenticate

from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers as user_serializers


class UserRegistrationAPIView(CreateAPIView):
    """
        success response format
         {
           first_name: "",
           last_name: "",
           email: "",
           date_joined: "",
           "token"
         }
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = user_serializers.UserRegistrationSerializer


class UserLoginAPIView(APIView):
    """
        success response format
         {
           auth_token: ""
         }
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email is None or password is None:
            return Response(
                {"error": "Please provide both email and password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"auth_token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST
            )
