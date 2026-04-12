import time

from django.core.management.base import BaseCommand
from django.conf import settings

from music.services.base_strategy import GenerationRequest
from music.services.strategy_selector import get_generator_strategy


DEMO_REQUEST = GenerationRequest(
    title         = 'Happy Birthday Song',
    occasion      = 'BIRTHDAY',
    genre         = 'POP',
    mood          = 'HAPPY',
    voice_type    = 'FEMALE',
    custom_lyrics = 'Wishing you a wonderful day full of joy and laughter.',
)


class Command(BaseCommand):
    help = 'Demonstrate song generation using the configured strategy (mock or suno).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--strategy',
            choices=['mock', 'suno'],
            default=None,
            help='Override GENERATOR_STRATEGY for this run.',
        )
        parser.add_argument(
            '--poll-interval',
            type=int,
            default=3,
            help='Seconds between status polls (default: 3).',
        )
        parser.add_argument(
            '--max-polls',
            type=int,
            default=10,
            help='Max number of status polls before giving up (default: 10).',
        )

    def handle(self, *args, **options):
        # Allow command-line override of strategy
        if options['strategy']:
            settings.GENERATOR_STRATEGY = options['strategy']

        active = getattr(settings, 'GENERATOR_STRATEGY', 'mock')
        self.stdout.write(self.style.MIGRATE_HEADING(
            f'\n=== Exercise 4 — Strategy Pattern Demo | strategy={active} ==='
        ))

        #instantiate the strategy
        try:
            strategy = get_generator_strategy()
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f'Failed to load strategy: {exc}'))
            return

        self.stdout.write(f'Strategy class : {type(strategy).__name__}')
        self.stdout.write(f'Request        : title={DEMO_REQUEST.title!r}')
        self.stdout.write(f'                 genre={DEMO_REQUEST.genre} | mood={DEMO_REQUEST.mood}')
        self.stdout.write(f'                 occasion={DEMO_REQUEST.occasion} | voice={DEMO_REQUEST.voice_type}')
        self.stdout.write('')

        # submit generation
        self.stdout.write('Submitting generation…')
        try:
            result = strategy.generate(DEMO_REQUEST)
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f'generate() failed: {exc}'))
            return

        self.stdout.write(self.style.SUCCESS(f'  task_id  : {result.task_id}'))
        self.stdout.write(f'  status   : {result.status}')
        self.stdout.write('')

        # poll for completion
        poll_interval = options['poll_interval']
        max_polls     = options['max_polls']

        for poll in range(1, max_polls + 1):
            if result.is_complete:
                break
            if result.is_failed:
                self.stderr.write(self.style.ERROR(f'Generation failed: {result.error}'))
                return

            self.stdout.write(f'  poll {poll}/{max_polls} — status={result.status} — waiting {poll_interval}s…')
            time.sleep(poll_interval)

            try:
                result = strategy.get_status(result.task_id)
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f'get_status() failed: {exc}'))
                return

        # report final result
        self.stdout.write('')
        if result.is_complete:
            self.stdout.write(self.style.SUCCESS('Generation complete!'))
            self.stdout.write(f'  final status : {result.status}')
            self.stdout.write(f'  audio_url    : {result.audio_url}')
            self.stdout.write(f'  duration     : {result.duration}s')
        else:
            self.stdout.write(self.style.WARNING(
                f'Did not reach SUCCESS within {max_polls} polls. '
                f'Last status: {result.status}'
            ))

        self.stdout.write('')