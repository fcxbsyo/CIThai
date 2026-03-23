from django.db import models
from .enums import GenerationStatus
from .user import User


class SongGeneration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generations')
    submitted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=GenerationStatus.choices,
        default=GenerationStatus.GENERATING
    )
    error_message = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.status} - {self.submitted_at}"