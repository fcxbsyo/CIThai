import threading
import uuid

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..models import Song, SongGeneration, ShareLink
from ..serializers import SongSerializer, SongGenerationSerializer

OFFENSIVE_WORDS = ['fuck', 'shit', 'nigger', 'faggot', 'cunt', 'bitch', 'racist', 'sexist']


class SongViewSet(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from ..models import SharedSongAccess
        owned = Song.objects.filter(owner=self.request.user)
        
        # if owned=true param, return only owned songs (for library My Songs section)
        if self.request.query_params.get('owned') == 'true':
            return owned
        
        # otherwise return owned + shared (for detail page access)
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
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(song.audio_file_reference)

    @action(detail=True, methods=['post'], url_path='share')
    def share(self, request, pk=None):
        song = self.get_object()

        # C-3: only allow share for READY songs
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


class SongGenerationViewSet(viewsets.ModelViewSet):
    serializer_class = SongGenerationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SongGeneration.objects.filter(user=self.request.user)


class GenerateSongView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from ..services.song_creation_service import SongCreationService
        from ..models import Genre, Occasion

        # C-2: 20 song limit
        song_count = Song.objects.filter(owner=request.user).count()
        if song_count >= 20:
            return Response(
                {'detail': 'You have reached the 20 song limit. Please delete some songs before creating new ones.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # NFR-P4: max 3 concurrent background generations
        active_generations = SongGeneration.objects.filter(
            user=request.user,
            status='GENERATING'
        ).count()
        if active_generations >= 3:
            return Response(
                {'detail': 'You have 3 songs currently generating. Please wait for them to complete before starting a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # NFR-S1: content filtering
        custom_lyrics = request.data.get('custom_lyrics', '') or ''
        lyrics_lower = custom_lyrics.lower()
        for word in OFFENSIVE_WORDS:
            if word in lyrics_lower:
                return Response(
                    {'detail': 'Lyrics contain offensive content. Please revise before submitting.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            genre = Genre.objects.get(id=request.data.get('genre'))
            occasion = Occasion.objects.get(id=request.data.get('occasion'))
        except (Genre.DoesNotExist, Occasion.DoesNotExist):
            return Response(
                {'detail': 'Invalid genre or occasion.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        generation = SongGeneration.objects.create(user=request.user)

        params = {
            'title': request.data.get('title'),
            'occasion': occasion.name,
            'genre': genre.name,
            'mood': request.data.get('mood'),
            'voice_type': request.data.get('voice_type', 'MALE'),
            'custom_lyrics': custom_lyrics,
        }

        def run():
            SongCreationService().submit_generation(generation, params)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

        return Response(
            SongGenerationSerializer(generation).data,
            status=status.HTTP_201_CREATED
        )