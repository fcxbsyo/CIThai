from django.db import models

class GenerationStatus(models.TextChoices):
    GENERATING = 'GENERATING', 'Generating'
    READY = 'READY', 'Ready'
    FAILED = 'FAILED', 'Failed'

class Mood(models.TextChoices):
    HAPPY = 'HAPPY', 'Happy'
    SAD = 'SAD', 'Sad'
    ROMANTIC = 'ROMANTIC', 'Romantic'
    ENERGETIC = 'ENERGETIC', 'Energetic'
    CALM = 'CALM', 'Calm'

class Genre(models.TextChoices):
    ROCK = 'ROCK', 'Rock'
    JAZZ = 'JAZZ', 'Jazz'
    RNB = 'RNB', 'R&B'
    POP = 'POP', 'Pop'
    CLASSICAL = 'CLASSICAL', 'Classical'
    HIPHOP = 'HIPHOP', 'Hip Hop'

class Occasion(models.TextChoices):
    BIRTHDAY = 'BIRTHDAY', 'Birthday'
    WEDDING = 'WEDDING', 'Wedding'
    CHRISTMAS = 'CHRISTMAS', 'Christmas'
    GRADUATION = 'GRADUATION', 'Graduation'
    ANNIVERSARY = 'ANNIVERSARY', 'Anniversary'
    OTHER = 'OTHER', 'Other'

class VoiceType(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    CHILD = 'CHILD', 'Child'
    CHOIR = 'CHOIR', 'Choir'
    INSTRUMENTAL = 'INSTRUMENTAL', 'Instrumental'
    DUET = 'DUET', 'Duet'