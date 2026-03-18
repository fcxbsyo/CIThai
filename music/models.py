from django.db import models
import uuid


# Enumerations
class Occasion(models.TextChoices):
    BIRTHDAY = 'BIRTHDAY', 'Birthday'
    ANNIVERSARY = 'ANNIVERSARY', 'Anniversary'
    GRADUATION = 'GRADUATION', 'Graduation'
    VALENTINE = 'VALENTINE', 'Valentine'
    OTHER = 'OTHER', 'Other'


class Genre(models.TextChoices):
    POP = 'POP', 'Pop'
    ROCK = 'ROCK', 'Rock'
    ACOUSTIC = 'ACOUSTIC', 'Acoustic'
    JAZZ = 'JAZZ', 'Jazz'
    OTHER = 'OTHER', 'Other'


class Mood(models.TextChoices):
    HAPPY = 'HAPPY', 'Happy'
    ROMANTIC = 'ROMANTIC', 'Romantic'
    EMOTIONAL = 'EMOTIONAL', 'Emotional'
    FUN = 'FUN', 'Fun'
    INSPIRATIONAL = 'INSPIRATIONAL', 'Inspirational'


class VoiceType(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    DUET = 'DUET', 'Duet'


class GenerationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'


# Domain Entities
class User(models.Model):
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.display_name} ({self.email})"


class SongGeneration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='song_generation')
    submitted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=GenerationStatus.choices, default=GenerationStatus.PENDING)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Generation by {self.user} [{self.status}] at {self.submitted_at}"


class Song(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    generation = models.OneToOneField(SongGeneration, on_delete=models.CASCADE, related_name='song')
    title = models.CharField(max_length=255)
    occasion = models.CharField(max_length=20, choices=Occasion.choices)
    genre = models.CharField(max_length=20, choices=Genre.choices)
    mood = models.CharField(max_length=20, choices=Mood.choices)
    voice_type = models.CharField(max_length=20, choices=VoiceType.choices)
    custom_lyrics = models.TextField(max_length=1500, blank=True, null=True)
    duration_seconds = models.PositiveIntegerField()
    audio_file_reference = models.CharField(max_length=500)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.title}" by {self.owner}'
    

class ShareLink(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='share_link')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"ShareLink for '{self.song.title}' ({'active' if self.is_active else 'inactive'})"