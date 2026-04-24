from rest_framework import serializers
from .models import User, Genre, Occasion, Song, SongGeneration, ShareLink


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'google_id', 'display_name', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'display_name', 'password']

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value
    
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            display_name=validated_data['display_name'],
            password=validated_data['password'],
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ['id', 'name']


class SongSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    occasion_name = serializers.CharField(source='occasion.name', read_only=True)

    def get_status(self, obj):
        if obj.generation:
            return obj.generation.status
        return 'READY'

    class Meta:
        model = Song
        fields = ['id', 'owner', 'generation', 'title', 'occasion', 'genre',
                  'mood', 'voice_type', 'custom_lyrics', 'duration_seconds',
                  'audio_file_reference', 'generated_at', 'updated_at',
                  'status', 'genre_name', 'occasion_name']
        read_only_fields = ['owner', 'generated_at', 'updated_at', 'status',
                            'genre_name', 'occasion_name']
        extra_kwargs = {
            'audio_file_reference': {'required': False, 'allow_blank': True, 'default': ''},
            'duration_seconds': {'required': False, 'default': 0},
        }
        

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
        

class ShareLinkPublicSerializer(serializers.ModelSerializer):
    owner_display_name = serializers.CharField(source='owner.display_name', read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'title', 'owner_display_name', 'occasion', 'genre',
                  'mood', 'duration_seconds', 'generated_at']