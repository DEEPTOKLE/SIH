import sys

from django.core.management.base import BaseCommand

from ip_sakti.seed_data import main


class Command(BaseCommand):
    help = 'Seed the database with demo data for IP-SAKTI'

    def handle(self, *args, **options):
        main()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))
        sys.exit(0)
