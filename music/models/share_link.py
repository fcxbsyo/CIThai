from django.db import models
from .song import Song


class ShareLink(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='share_link')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"ShareLink ({self.token})"