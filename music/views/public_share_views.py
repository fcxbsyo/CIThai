from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from ..models import ShareLink
from ..serializers import ShareLinkPublicSerializer


class PublicShareView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        share_link = get_object_or_404(ShareLink, token=token, is_active=True)
        return Response(ShareLinkPublicSerializer(share_link.song, context={'request': request}).data)