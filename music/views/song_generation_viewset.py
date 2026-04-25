from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import SongGeneration
from ..serializers import SongGenerationSerializer


class SongGenerationViewSet(viewsets.ModelViewSet):
    serializer_class = SongGenerationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SongGeneration.objects.filter(user=self.request.user)