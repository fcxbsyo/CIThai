from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import SongSerializer


class SharedWithMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from ..models import SharedSongAccess
        accesses = SharedSongAccess.objects.filter(
            user=request.user
        ).exclude(
            share_link__song__owner=request.user
        ).select_related('share_link__song', 'share_link__song__owner')
        songs = [a.share_link.song for a in accesses]
        return Response(SongSerializer(songs, many=True).data)