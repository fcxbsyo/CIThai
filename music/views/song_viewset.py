import uuid
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import StreamingHttpResponse

from ..models import Song, ShareLink
from ..serializers import SongSerializer


class SongViewSet(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from ..models import SharedSongAccess
        owned = Song.objects.filter(owner=self.request.user)
        if self.request.query_params.get('owned') == 'true':
            return owned
        shared_ids = SharedSongAccess.objects.filter(
            user=self.request.user
        ).values_list('share_link__song_id', flat=True)
        shared = Song.objects.filter(id__in=shared_ids)
        return (owned | shared).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        song = self.get_object()
        if not song.audio_file_reference:
            return Response(
                {'detail': 'Audio file not available yet.'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            r = requests.get(song.audio_file_reference, stream=True, timeout=30)
            r.raise_for_status()
            content_type = r.headers.get('Content-Type', 'audio/mpeg')
            response = StreamingHttpResponse(r.iter_content(chunk_size=8192), content_type=content_type)
            filename = f"{song.title}.mp3".replace('"', '')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            if 'Content-Length' in r.headers:
                response['Content-Length'] = r.headers['Content-Length']
            return response
        except Exception:
            return Response({'detail': 'Download failed.'}, status=status.HTTP_502_BAD_GATEWAY)

    @action(detail=True, methods=['post'], url_path='share')
    def share(self, request, pk=None):
        song = self.get_object()
        if song.generation and song.generation.status != 'READY':
            return Response(
                {'detail': 'Share link can only be generated for ready songs.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        share_link, created = ShareLink.objects.get_or_create(
            song=song,
            defaults={'token': uuid.uuid4().hex}
        )
        if not created and not share_link.is_active:
            share_link.is_active = True
            share_link.save(update_fields=['is_active'])
        return Response(
            {
                'token': share_link.token,
                'share_url': request.build_absolute_uri(f'/api/share/{share_link.token}/'),
                'is_active': share_link.is_active,
            },
            status=status.HTTP_200_OK
        )