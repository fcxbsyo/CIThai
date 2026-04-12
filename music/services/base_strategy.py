from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class GenerationRequest:
    title: str
    occasion: str
    genre: str
    mood: str
    voice_type: str
    custom_lyrics: Optional[str] = ''


@dataclass
class GenerationResult:
    """
    Output value object returned by every strategy.
 
    task_id - ID returned by the external service (or a synthetic ID for the mock strategy). 
              Used for status polling.

    status - Current status string as returned by the service 
              (e.g. 'PENDING', 'SUCCESS', 'mock_complete').

    audio_url - Publicly reachable MP3 URL once generation is complete. 
                Empty string while still in progress.

    duration - Duration in seconds once complete; 0 while in progress.
    
    error - Human-readable error message on failure; empty string on success.
    """
    task_id: str
    status: str
    audio_url: str = ''
    duration: int = 0
    error: str = ''

    @property
    def is_complete(self) -> bool:
        return self.status == 'SUCCESS' or self.status == 'mock_complete'
    
    @ property
    def is_failed(self) -> bool:
        return self.status in ('FAILED', 'ERROR', 'mock_error')
    

class SongGeneratorStrategy(ABC):

    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Submit a song-generation task and return an initial result.
 
        This method should return quickly (i.e. not block until the song
        is finished).  The returned GenerationResult.task_id can then be
        passed to get_status() for polling.
 
        Args:
            request: Validated domain parameters for the song.
 
        Returns:
            GenerationResult with at minimum a task_id and initial status.
        """
    
    @abstractmethod
    def get_status(self, task_id: str) -> GenerationResult:
        """
        Retrieve the current status of a previously submitted task.
 
        Args:
            task_id: The identifier returned by generate().
 
        Returns:
            Updated GenerationResult.  If is_complete is True the result
            also carries audio_url and duration.
        """