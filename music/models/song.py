from django.db import models
from .enums import Mood, Genre, Occasion, VoiceType
from .user import User

class Song(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    generation = models.OneToOneField(
        'SongGeneration',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='produced_song'
    )
    title = models.CharField(max_length=255)
    occasion = models.CharField(max_length=50, choices=Occasion.choices)
    genre = models.CharField(max_length=50, choices=Genre.choices)
    mood = models.CharField(max_length=50, choices=VoiceType.choices)
    custom_lyrics = models.TextField(max_length=1500, null=True, blank=True)
    duration_seconds = models.IntegerField()
    audio_file_reference = models.CharField(max_length=500)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title