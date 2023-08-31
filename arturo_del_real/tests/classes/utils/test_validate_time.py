from datetime import time
from unittest import TestCase

from utils import validate_time


class ValidateTimeTest(TestCase):

    def test_should_get_correct_time(self):
        correct_time = validate_time('09:30')
        self.assertTrue(correct_time.is_ok())
        self.assertEqual(correct_time.ok(), time(9, 30))

    def test_should_get_incorrect_time(self):
        incorrect_time = validate_time('25:30')
        self.assertTrue(incorrect_time.is_err())
        self.assertEqual(incorrect_time.err(), 'Invalid date')
