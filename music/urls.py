from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet, SongGenerationViewSet, ShareLinkViewSet, GenreViewSet, OccasionViewSet

router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'generations', SongGenerationViewSet)
router.register(r'sharelinks', ShareLinkViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'occasions', OccasionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]