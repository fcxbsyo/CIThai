import logging
import requests
from django.conf import settings

from .base_strategy import SongGeneratorStrategy, GenerationRequest, GenerationResult
from ..models.enums import Mood, VoiceType

logger = logging.getLogger(__name__)

GENRE_TAG: dict[str, str] = {
    'Rock':      'rock, electric guitar, drums',
    'Jazz':      'jazz, saxophone, piano, swing',
    'R&B':       'r&b, soul, smooth vocals',
    'Pop':       'pop, catchy, radio-friendly',
    'Classical': 'classical, orchestral, strings',
    'Hip Hop':   'hip hop, rap, urban beat',
}

MOOD_TAG: dict[str, str] = {
    Mood.HAPPY:     'upbeat, cheerful, joyful',
    Mood.SAD:       'melancholic, emotional, slow',
    Mood.ROMANTIC:  'romantic, tender, intimate',
    Mood.ENERGETIC: 'energetic, fast tempo, powerful',
    Mood.CALM:      'calm, peaceful, relaxing',
}

VOICE_TAG: dict[str, str] = {
    VoiceType.MALE:         'male vocals, baritone',
    VoiceType.FEMALE:       'female vocals, soprano',
    VoiceType.CHILD:        "children's choir, pure",
    VoiceType.CHOIR:        'choir, harmonies, ensemble',
    VoiceType.INSTRUMENTAL: 'instrumental, no vocals',
    VoiceType.DUET:         'male and female duet',
}

OCCASION_PROMPT: dict[str, str] = {
    'Birthday':    'a joyful birthday celebration song',
    'Wedding':     'a beautiful wedding ceremony song',
    'Christmas':   'a warm christmas holiday song',
    'Graduation':  'an inspiring graduation achievement song',
    'Anniversary': 'a heartfelt anniversary love song',
    'Other':       'a meaningful personal occasion song',
}

IN_PROGRESS_STATUSES = {'PENDING', 'TEXT_SUCCESS', 'FIRST_SUCCESS'}


class SunoStrategyError(Exception):
    """Raised on unrecoverable errors communicating with SunoAPI.org."""


class SunoSongGeneratorStrategy(SongGeneratorStrategy):

    BASE_URL = 'https://api.sunoapi.org/api/v1'

    def __init__(self):
        self.api_key = getattr(settings, 'SUNO_API_KEY', '')
        if not self.api_key:
            raise SunoStrategyError(
                'SUNO_API_KEY is not configured. '
                'Set it as an environment variable before using the Suno strategy.'
            )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        payload = self._build_payload(request)

        logger.info(
            '[SunoStrategy] Submitting generation | title=%r | tags=%s',
            request.title,
            payload.get('tags', ''),
        )

        try:
            response = requests.post(
                f'{self.BASE_URL}/generate',
                json=payload,
                headers=self._headers(),
                timeout=30,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise SunoStrategyError(f'SunoAPI generation request failed: {exc}') from exc

        data = response.json()
        inner = data.get('data') or {}
        task_id = inner.get('taskId') or inner.get('task_id') or ''

        if not task_id:
            raise SunoStrategyError(
                f'SunoAPI response did not contain a taskId. Response: {data}'
            )

        logger.info('[SunoStrategy] Task submitted | task_id=%s', task_id)

        return GenerationResult(
            task_id=task_id,
            status='PENDING',
        )

    def get_status(self, task_id: str) -> GenerationResult:
        logger.info('[SunoStrategy] Polling status | task_id=%s', task_id)

        try:
            response = requests.get(
                f'{self.BASE_URL}/generate/record-info',
                params={'taskId': task_id},
                headers=self._headers(),
                timeout=15,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise SunoStrategyError(f'SunoAPI status poll failed: {exc}') from exc

        data = response.json()
        inner = data.get('data') or {}
        task_id = inner.get('taskId') or inner.get('task_id') or ''
        status = inner.get('status', 'PENDING')

        # correct path: data.response.sunoData
        audio_url = ''
        duration = 0

        if status == 'SUCCESS':
            suno_data = inner.get('response', {}).get('sunoData', [])
            if suno_data:
                first_clip = suno_data[0]
                audio_url = first_clip.get('audioUrl', '')
                duration = int(first_clip.get('duration', 0) or 0)

        logger.info(
            '[SunoStrategy] Poll result | task_id=%s | status=%s | audio_url=%s',
            task_id, status, audio_url or '(not yet ready)',
        )

        return GenerationResult(
            task_id=task_id,
            status=status,
            audio_url=audio_url,
            duration=duration,
        )

    def _headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type':  'application/json',
            'Accept':        'application/json',
        }

    def _build_payload(self, request: GenerationRequest) -> dict:
        prompt = self._build_prompt(request)
        tags   = self._build_tags(request)

        payload: dict = {
            'title':        request.title,
            'prompt':       prompt,
            'tags':         tags,
            'model':        'V4',
            'customMode':   False,
            'instrumental': False,
            'callBackUrl':  getattr(settings, 'SUNO_CALLBACK_URL', ''),
        }

        return payload

    @staticmethod
    def _build_prompt(request: GenerationRequest) -> str:
        occasion_desc = OCCASION_PROMPT.get(request.occasion, 'a special occasion song')
        parts = [f'Create {occasion_desc}.']
        if request.custom_lyrics:
            parts.append(f'Incorporate this theme or story: {request.custom_lyrics.strip()}')
        return ' '.join(parts)

    @staticmethod
    def _build_tags(request: GenerationRequest) -> str:
        parts = [
            GENRE_TAG.get(request.genre,      'pop'),
            MOOD_TAG.get(request.mood,        'upbeat'),
            VOICE_TAG.get(request.voice_type, 'vocals'),
        ]
        return ', '.join(parts)