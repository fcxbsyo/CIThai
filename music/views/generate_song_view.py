import threading
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..models import Song, SongGeneration
from ..serializers import SongGenerationSerializer

OFFENSIVE_WORDS = ['fuck', 'shit', 'nigger', 'faggot', 'cunt', 'bitch', 'racist', 'sexist']


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