import uuid
from collections import defaultdict

from .base_strategy import SongGeneratorStrategy, GenerationRequest, GenerationResult


MOCK_AUDIO_URL = 'http://localhost:8000/static/music/placeholder.mp3'
MOCK_DURATION_SECS = 30


class MockSongGeneratorStrategy(SongGeneratorStrategy):

    _poll_counts: dict[str, int] = defaultdict(int)

    def generate(self, request: GenerationRequest) -> GenerationResult:
        import logging
        logger = logging.getLogger(__name__)
        task_id = f'mock-{uuid.uuid4().hex[:12]}'

        logger.info(
            '[MockStrategy] generate() called | task_id=%s | title=%r | '
            'genre=%s | mood=%s | voice_type=%s | occasion=%s | lyrics=%r',
            task_id,
            request.title,
            request.genre,
            request.mood,
            request.voice_type,
            request.occasion,
            (request.custom_lyrics or '')[:80],
        )

        self._poll_counts[task_id] = 0

        return GenerationResult(
            task_id=task_id,
            status='PENDING',
        )
    
    def get_status(self, task_id: str) -> GenerationResult:
        import logging
        logger = logging.getLogger(__name__)

        self._poll_counts[task_id] += 1
        count = self._poll_counts[task_id]

        if count < 2:
            logger.info('[MockStrategy] get_status() | task_id=%s | poll=%d → PENDING', task_id, count)
            return GenerationResult(task_id=task_id, status='PENDING')
        
        logger.info('[MockStrategy] get_status() | task_id=%s | poll=%d → SUCCESS', task_id, count)
        return GenerationResult(
            task_id=task_id,
            status='SUCCESS',
            audio_url=MOCK_AUDIO_URL,
            duration=MOCK_DURATION_SECS,
        )