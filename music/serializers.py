from rest_framework import serializers
from .models import User, Genre, Occasion, Song, SongGeneration, ShareLink


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'google_id', 'display_name', 'created_at']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ['id', 'name']


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'owner', 'generation', 'title', 'occasion', 'genre',
                  'mood', 'voice_type', 'custom_lyrics', 'duration_seconds',
                  'audio_file_reference', 'generated_at', 'updated_at']
        

class SongGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGeneration
        fields = ['id', 'user', 'submitted_at', 'completed_at', 'status', 
                  'error_message', 'updated_at']
        

class ShareLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareLink
        fields = ['id', 'song', 'token', 'created_at', 'is_active',
                  'expires_at', 'deactivated_at']