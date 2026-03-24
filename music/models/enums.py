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

class VoiceType(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    CHILD = 'CHILD', 'Child'
    CHOIR = 'CHOIR', 'Choir'
    INSTRUMENTAL = 'INSTRUMENTAL', 'Instrumental'
    DUET = 'DUET', 'Duet'