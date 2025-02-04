from django.contrib.auth import authenticate

from rest_framework import status
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
    serializer_class = user_serializers.UserRegistrationSerializer


class UserLoginAPIView(APIView):
    """
        success response format
         {
           auth_token: ""
         }
    """

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        try:
            user = authenticate(username=email, password=password)
            
            if user: 
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"auth_token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
