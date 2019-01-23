"""
./manage.py teryt_flush 
------------

Command will remove all teryt data from datebase
"""

from django.core.management.base import BaseCommand, CommandError

from teryt.models import *


class Command(BaseCommand):
    help = 'Remove all teryt data from datebase'

    def handle(self, *args, **options):
        JednostkaAdministracyjna.objects.all().delete()
        Miejscowosc.objects.all().delete()
        RodzajMiejscowosci.objects.all().delete()
        Ulica.objects.all().delete()
        self.stdout.write('Data flushed...')
