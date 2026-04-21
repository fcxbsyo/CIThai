from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from ..models import ShareLink
from ..serializers import ShareLinkSerializer, ShareLinkPublicSerializer


class ShareLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ShareLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShareLink.objects.filter(song__owner=self.request.user)


class PublicShareView(APIView):
    """
    FR32: Anyone can view song metadata via share token, no login required.
    FR33/FR34: Audio URL is withheld; playback requires authentication.
    """
    permission_classes = [AllowAny]

    def get(self, request, token):
        share_link = get_object_or_404(ShareLink, token=token, is_active=True)
        serializer = ShareLinkPublicSerializer(share_link.song, context={'request': request})
        return Response(serializer.data)