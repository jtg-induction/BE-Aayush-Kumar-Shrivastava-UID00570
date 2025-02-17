from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView

from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

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

    permission_classes = []
    serializer_class = user_serializers.UserRegistrationSerializer


class UserLoginAPIView(GenericAPIView):
    """
        success response format
         {
           auth_token: ""
         }
    """

    permission_classes = []
    serializer_class = user_serializers.UserLoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid(raise_exception=True): 
            raise serializers.ValidationError(
                {"error": "Invalid credentials."},
                code=status.HTTP_400_BAD_REQUEST
              )
        
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({"auth_token": token.key}, status=status.HTTP_200_OK)
