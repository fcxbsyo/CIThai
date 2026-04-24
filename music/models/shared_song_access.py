from django.db import models
from .user import User
from .share_link import ShareLink


class SharedSongAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_accesses')
    share_link = models.ForeignKey(ShareLink, on_delete=models.CASCADE, related_name='accesses')
    accessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'share_link')

    def __str__(self):
        return f"{self.user} accessed {self.share_link}"