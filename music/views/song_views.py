from rest_framework import viewsets
from ..models import Song, SongGeneration
from ..serializers import SongSerializer, SongGenerationSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongGenerationViewSet(viewsets.ModelViewSet):
    queryset = SongGeneration.objects.all()
    serializer_class = SongGenerationSerializer