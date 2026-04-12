from django.conf import settings
from .base_strategy import SongGeneratorStrategy
from .mock_strategy import MockSongGeneratorStrategy
from .suno_strategy import SunoSongGeneratorStrategy


STRATEGY_MOCK = 'mock'
STRATEGY_SUNO = 'suno'

_REGISTRY: dict[str, type[SongGeneratorStrategy]] = {
    STRATEGY_MOCK: MockSongGeneratorStrategy,
    STRATEGY_SUNO: SunoSongGeneratorStrategy,
}


def get_generator_strategy() -> SongGeneratorStrategy:
    strategy_name = getattr(settings, 'GENERATOR_STRATEGY', STRATEGY_MOCK).strip().lower()
    strategy_class = _REGISTRY.get(strategy_name)
    if strategy_class is None:
        raise ValueError(
            f"Unknown GENERATOR_STRATEGY '{strategy_name}'. "
            f"Valid options: {', '.join(_REGISTRY.keys())}"
        )
    return strategy_class()