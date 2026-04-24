from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    SongViewSet, SongGenerationViewSet, GenerateSongView,
    ShareLinkViewSet, GenreViewSet, 
    OccasionViewSet, PublicShareView, SharedWithMeView,
    RegisterView, LoginView)

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')
router.register(r'generations', SongGenerationViewSet, basename='songgeneration')
router.register(r'sharelinks', ShareLinkViewSet, basename='sharelink')
router.register(r'genres', GenreViewSet)
router.register(r'occasions', OccasionViewSet)

urlpatterns = [
    path('songs/shared-with-me/', SharedWithMeView.as_view(), name='shared-with-me'),
    path('generate/', GenerateSongView.as_view(), name='generate-song'),
    path('', include(router.urls)),
    path('share/<str:token>/', PublicShareView.as_view(), name='public-share'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh')
]