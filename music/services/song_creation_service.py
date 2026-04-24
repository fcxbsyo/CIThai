import time
import logging

from django.utils import timezone

from ..models import Song, SongGeneration
from ..models.enums import GenerationStatus, VoiceType
from .base_strategy import GenerationRequest, GenerationResult
from .strategy_selector import get_generator_strategy

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 10
MAX_POLL_ATTEMPTS = 60


class SongCreationService:

    def submit_generation(self, generation: SongGeneration, params: dict) -> Song:
        from ..models import Genre, Occasion

        request = GenerationRequest(
            title=params['title'],
            occasion=params['occasion'],
            genre=params['genre'],
            mood=params['mood'],
            voice_type=params.get('voice_type', VoiceType.MALE),
            custom_lyrics=params.get('custom_lyrics', '') or '',
        )

        strategy = get_generator_strategy()
        logger.info('[SongCreationService] Using strategy: %s', type(strategy).__name__)

        try:
            result = self._generate_and_wait(strategy, request)
        except Exception as exc:
            logger.warning('[SongCreationService] First attempt failed: %s, retrying...', exc)
            try:
                result = self._generate_and_wait(strategy, request)
            except Exception as exc2:
                generation.status = GenerationStatus.FAILED
                generation.error_message = str(exc2)
                generation.save(update_fields=['status', 'error_message', 'updated_at'])
                raise

        genre_obj = Genre.objects.get(name=params['genre'])
        occasion_obj = Occasion.objects.get(name=params['occasion'])

        song = Song.objects.create(
            owner=generation.user,
            generation=generation,
            title=params['title'],
            occasion=occasion_obj,
            genre=genre_obj,
            mood=params['mood'],
            voice_type=params.get('voice_type', VoiceType.MALE),
            custom_lyrics=params.get('custom_lyrics', '') or '',
            audio_file_reference=result.audio_url,
            duration_seconds=result.duration,
        )

        generation.status = GenerationStatus.READY
        generation.completed_at = timezone.now()
        generation.save(update_fields=['status', 'completed_at', 'updated_at'])

        logger.info('[SongCreationService] Song created | song_id=%s', song.id)
        return song

    def _generate_and_wait(self, strategy, request: GenerationRequest) -> GenerationResult:
        result = strategy.generate(request)

        for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
            if result.is_complete:
                return result
            if result.is_failed:
                raise RuntimeError(f'Strategy reported failure: {result.error}')
            logger.debug('[SongCreationService] Polling | attempt=%d | status=%s', attempt, result.status)
            time.sleep(POLL_INTERVAL_SECONDS)
            result = strategy.get_status(result.task_id)

        raise TimeoutError(f'Generation timed out after {MAX_POLL_ATTEMPTS * POLL_INTERVAL_SECONDS}s')