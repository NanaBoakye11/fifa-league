

import csv
from django.core.management.base import BaseCommand
from core.models import Player

class Command(BaseCommand):
    help = 'Import player names from a CSV exported from Google Forms'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header

            for row in reader:
                name = row[0].strip()
                if not Player.objects.filter(name=name).exists():
                    Player.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f'✅ Added: {name}'))
                else:
                    self.stdout.write(f'⏭ Skipped duplicate: {name}')
