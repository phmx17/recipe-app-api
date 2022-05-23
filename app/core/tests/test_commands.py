"""
Test custom Django management commands
"""
from unittest.mock import patch # used to mock the behavior of db

from psycopg2 import OperationalError as Psycopg2Error # catch exception from trying to connect when db is not ready yet

from django.core.management import call_command # helper function to call a command by name
from django.db.utils import OperationalError # another possible exception that can get thrown
from django.test import SimpleTestCase # for unit testing

@patch('core.management.commands.wait_for_db.Command.check') # decorator that enables mocking; .check() is a Command method that checks db
class CommandTests(SimpleTestCase):
  """Test commands"""

  def test_wait_for_db_ready(self, patched_check):
    """Test waiting for database if db ready"""
    patched_check.return_value = True

    call_command('wait_for_db')

    patched_check.assert_called_once_with(databases=['default'])
  
  # exceptions for when db is not ready
  @patch('time.sleep')
  def test_wait_for_db_delay(self, patched_sleep, patched_check): # patched_sleep must come before patched_check; params from decorators get added from the inside outwards;
    """Test waiting for database when getting operational error"""
    patched_check.side_effect = [Psycopg2Error] * 2 + \
      [OperationalError] * 3 + [True] # raise 3 operational errors and 2 psycop errors; these vals are arbitrary!; return True at 6th time of calling, instead of raising exception

    call_command('wait_for_db')
    
    self.assertEqual(patched_check.call_count, 6) # assert that mocked check method got called total of 6 times (2+3+True)
    patched_check.assert_called_with(databases=['default'])

    # mock sleep method between db checks in order to prevent over-checking; but we don't actually wait for sleep to complete!

