from rest_framework import viewsets
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


class RecordShareAccessView(APIView):
    """Record when a logged-in user accesses a shared song."""
    permission_classes = [IsAuthenticated]

    def post(self, request, token):
        from ..models import SharedSongAccess
        share_link = get_object_or_404(ShareLink, token=token, is_active=True)
        SharedSongAccess.objects.get_or_create(
            user=request.user,
            share_link=share_link
        )
        return Response({'status': 'ok'})


class SharedWithMeView(APIView):
    """FR31: Songs shared with the current user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from ..models import SharedSongAccess
        accesses = SharedSongAccess.objects.filter(
            user=request.user
        ).exclude(
            share_link__song__owner=request.user
        ).select_related('share_link__song', 'share_link__song__owner')

        songs = [a.share_link.song for a in accesses]
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)