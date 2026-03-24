from django.contrib import admin
from .models import User, Song, SongGeneration, ShareLink, Genre, Occasion
# Register your models here.

admin.site.register(User)
admin.site.register(Song)
admin.site.register(SongGeneration)
admin.site.register(ShareLink)
admin.site.register(Genre)
admin.site.register(Occasion)