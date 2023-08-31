from datetime import time
from unittest import TestCase

from main import Student, Attendance


class StudentTest(TestCase):

    def setUp(self):
        self.data = [
            '1',
            '09:10',
            '10:10',
            'Classroom'
        ]
        self.student = Student('Arthur')

    def test_add_data_should_add_new_attendance(self):
        self.student.add_data(self.data)
        expected_attendances = {
            1: [Attendance(1, time(9, 10), time(10, 10), 'Classroom')]
        }
        self.assertEqual(self.student.attendances, expected_attendances)

    def test_should_omit_data_wrong_day(self):
        self.data[0] = '0'
        self.student.add_data(self.data)
        expected_attendances = {}
        self.assertEqual(self.student.attendances, expected_attendances)

    def test_should_omit_data_not_integer_day(self):
        self.data[0] = 'not an integer'
        self.student.add_data(self.data)
        expected_attendances = {}
        self.assertEqual(self.student.attendances, expected_attendances)

    def test_should_omit_less_than_5_minutes(self):
        self.data[2] = '09:12'
        self.student.add_data(self.data)
        expected_attendances = {}
        self.assertEqual(self.student.attendances, expected_attendances)

    def test_should_omit_invalid_init_date(self):
        self.data[1] = '99:111'
        self.student.add_data(self.data)
        expected_attendances = {}
        self.assertEqual(self.student.attendances, expected_attendances)

    def test_should_omit_invalid_end_date(self):
        self.data[1] = 'i am clearly not a date'
        self.student.add_data(self.data)
        expected_attendances = {}
        self.assertEqual(self.student.attendances, expected_attendances)

    def test_should_get_total_minutes(self):
        self.student.add_data(self.data)
        self.data[0] = '2'
        self.student.add_data(self.data)

        self.data[1] = '18:11'
        self.data[2] = '20:00'

        self.student.add_data(self.data)
        self.assertEqual(self.student.total_minutes, 229)

    def test_should_get_days_present(self):
        self.student.add_data(self.data)
        self.data[0] = '2'
        self.student.add_data(self.data)

        self.data[1] = '18:11'
        self.data[2] = '20:00'

        self.student.add_data(self.data)
        self.assertEqual(self.student.days_present, 2)

    def test_should_get_empty_resume(self):
        expected_resume = 'Arthur: 0 minutes'
        self.assertEqual(self.student.get_resume(), expected_resume)

    def test_should_get_resume_in_single_day(self):
        self.student.add_data(self.data)
        expected_resume = 'Arthur: 60 minutes in 1 day'
        self.assertEqual(self.student.get_resume(), expected_resume)

    def test_should_get_resume_in_many_days(self):
        self.student.add_data(self.data)
        self.data[0] = '2'
        self.student.add_data(self.data)
        expected_resume = 'Arthur: 120 minutes in 2 days'
        self.assertEqual(self.student.get_resume(), expected_resume)
