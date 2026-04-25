from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect


class GoogleOAuthCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('http://localhost:5173/login?error=oauth_failed')
        refresh = RefreshToken.for_user(request.user)
        return redirect(
            f'http://localhost:5173/oauth-callback?access={str(refresh.access_token)}&refresh={str(refresh)}'
        )