"""
Django command in order to instruct Django to wait for database
"""

import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError # error django raises when db not ready
from django.core.management.base import BaseCommand

class Command(BaseCommand):
  """django command to wait for database"""

  def handle(self, *args, **options):
    """entry point for command"""
    self.stdout.write('Waiting for database...') # log to console
    db_up = False
    while db_up is False: # loop and check connection every second
      try:
        self.check(databases=['default'])
        db_up = True
      except (Psycopg2OpError, OperationalError):
        self.stdout.write('Database unavailable, waiting 1 second...')
        time.sleep(1)
    
    self.stdout.write(self.style.SUCCESS('Database available!'))
      