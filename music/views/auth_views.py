from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from ..models import User
from ..serializers import UserSerializer, RegisterSerializer


class RegisterView(APIView):
    """
    FR1: Register with email and password
    FR7: Account created. User can access their songs from any device via JWT
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_201_CREATED
        )
    

class LoginView(APIView):
    """
    FR2: Log in with email and password
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        if not email or not password:
            return Response(
                {'detail': 'Email and password are required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is None:
            return Response(
                {'detail': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(authenticated_user)
        return Response(
            {
                'user': UserSerializer(authenticated_user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        )