from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run migrations on startup'

    def handle(self, *args, **kwargs):
        self.stdout.write('Running migrations...')
        call_command('migrate', '--noinput')
        self.stdout.write(self.style.SUCCESS('Migrations completed successfully!'))