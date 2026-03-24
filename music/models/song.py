from django.db import models
from .enums import Mood, VoiceType
from .user import User
from .genre import Genre
from .occasion import Occasion

class Song(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    generation = models.OneToOneField(
        'SongGeneration',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='produced_song'
    )
    title = models.CharField(max_length=255)
    occasion = models.ForeignKey(Occasion, on_delete=models.PROTECT, related_name='songs')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='songs')
    mood = models.CharField(max_length=50, choices=Mood.choices)
    voice_type = models.CharField(max_length=50, choices=VoiceType.choices, default=VoiceType.MALE)
    custom_lyrics = models.TextField(max_length=1500, null=True, blank=True)
    duration_seconds = models.IntegerField()
    audio_file_reference = models.CharField(max_length=500)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title