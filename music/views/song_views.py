from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import  Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
import uuid

from ..models import Song, SongGeneration
from ..serializers import SongSerializer, SongGenerationSerializer


class SongViewSet(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # FR5, FR6: only return songs owned by the requesting user
        return Song.objects.filter(owner=self.request.user)
    
    def perform_destroy(self, instance):
        # FR16, FR17: only owner can delete (ownership already enforced by get_queryset)
        instance.delete()
    
    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        # FR29: redirect to the audio file URL
        song = self.get_object()
        if not song.audio_file_references:
            return Response(
                {'detail': 'Audio file not available yet.'},
                status=status.HTTP_404_NOT_FOUND
            )
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(song.audio_file_reference)
    
    @action(detail=True, methods=['post'], url_path='share')
    def share(self, request, pk=None):
        # FR30: generate a unique share link for this song
        song = self.get_object()
        share_link, created = ShareLink.objects.get_or_create(
            song=song,
            defaults={'token': uuid.uuid4().hex}
        )
        if not created and not share_link.is_active:
            # reactive if it was deactivated
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