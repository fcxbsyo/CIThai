import time
import logging 

from django.utils import timezone

from ..models import Song, SongGeneration
from ..models.enums import GenerationStatus, VoiceType
from .base_strategy import GenerationRequest, GenerationResult
from .strategy_selector import get_generator_strategy

logger = logging.getLogger(__name__)

# Polling settings
POLL_INTERVAL_SECONDS = 10
MAX_POLL_ATTEMPTS = 60


class SongCreationService:
    """
    Orchestrates the full song-generation pipeline (UC-03).
 
    1. Translates validated form params into a GenerationRequest.
    2. Calls strategy.generate() to submit the task.
    3. Polls strategy.get_status() until complete (with 10-min timeout).
    4. Persists Song and updates SongGeneration status.
 
    One automatic retry is performed on failure (UC-03 ext. 19a).
    """

    def submit_generation(self, generation: SongGeneration, params: dict) -> Song:
        """
        Run the full generation pipeline in a background thread.
 
        Args:
            generation: SongGeneration record (must be in GENERATING status).
            params:     Validated dict from SongCreationInputSerializer.
 
        Returns:
            The newly created Song.
 
        Raises:
            Exception: After two failed attempts; generation is marked FAILED.
        """
        request = GenerationRequest(
            title = params['title'],
            occasion = params['occasion'],
            genre = params['genre'],
            mood = params['mood'],
            voice_type = params.get('voice_type', VoiceType.MALE),
            custom_lyrics = params.get('custom_lyrics', '') or '',
        )

        strategy = get_generator_strategy()
        logger.info(
            '[SongCreationService] Using strategy: %s | generation_id=%s',
            type(strategy).__name__,
            generation.id,
        )

        # first attempt
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

        # persist Song
        song = Song.objects.create(
            owner = generation.user,
            generation = generation,
            title = params['title'],
            occasion = params['occasion'],
            genre = params['genre'],
            mood = params['mood'],
            voice_type = params.get('voice_type', VoiceType.MALE),
            custom_lyrics = params.get('custom_lyrics', '') or '',
            audio_file_reference = result.audio_url,
        )
        
        generation.status = GenerationStatus.READY
        generation.completed_at = timezone.now()
        generation.save(update_fields=['status', 'completed_at', 'updated_at'])

        logger.info(
            '[SongCreationService] Song created | song_id=%s | task_id=%s',
            song.id, result.task_id,
        )
        return song


    # Private helpers
    def _generate_and_wait(self, strategy, request: GenerationRequest) -> GenerationResult:
        """Submit a generation task and poll until complete or timeout."""
        result = strategy.generate(request)

        for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
            if result.is_complete:
                return result
            if result.is_failed:
                raise RuntimeError(
                    f'Strategy reportef failure on task {result.task_id}: {result.error}'
                )
            logger.debug(
                '[SongCreationService] Polling | task_id=%s | attempt=%d | status=%s',
                result.task_id, attempt, result.status,
            )
            time.sleep(POLL_INTERVAL_SECONDS)
            result = strategy.get_status(result.task_id)

        raise TimeoutError(
            f'Generation timed out after {MAX_POLL_ATTEMPTS * POLL_INTERVAL_SECONDS}s '
            f'(task_id={result.task_id})'
        )