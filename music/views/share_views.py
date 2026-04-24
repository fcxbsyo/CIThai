from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from ..models import ShareLink
from ..serializers import ShareLinkSerializer, ShareLinkPublicSerializer, SongSerializer


class ShareLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ShareLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShareLink.objects.filter(song__owner=self.request.user)


class PublicShareView(APIView):
    """FR32: Anyone can view song metadata via share token — no login required."""
    permission_classes = [AllowAny]

    def get(self, request, token):
        share_link = get_object_or_404(ShareLink, token=token, is_active=True)
        serializer = ShareLinkPublicSerializer(share_link.song, context={'request': request})
        return Response(serializer.data)


class SharedWithMeView(APIView):
    """FR31: Songs shared with the current user via share links they have accessed."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return all active share links that belong to OTHER users
        share_links = ShareLink.objects.filter(
            is_active=True
        ).exclude(
            song__owner=request.user
        ).select_related('song', 'song__owner')

        songs = [sl.song for sl in share_links]
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)