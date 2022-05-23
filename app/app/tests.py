"""
Sample tests
"""

from django.test import SimpleTestCase

from app import calc

class CalcTests(SimpleTestCase): # inherits 
  # test the calc module

  def test_add_numbers(self):
    res = calc.add(6, 5)
    # make assertion
    self.assertEqual(res, 11)

  def test_subtract_numbers(self):
    res = calc.subtract(10, 15)
    # make assertion
    self.assertEqual(res, 5)
