from datetime import time
from unittest import TestCase

from main import Attendance


class AttendanceTest(TestCase):

    def test_should_consider_attendance(self):
        attendance = Attendance(1, time(9, 10), time(9, 15), 'Classroom')
        self.assertTrue(attendance.consider())

    def test_should_not_consider_attendance(self):
        attendance = Attendance(1, time(0, 59), time(1, 3), 'Classroom')
        self.assertFalse(attendance.consider())

    def test_should_get_correct_minutes(self):
        attendance = Attendance(1, time(0, 59), time(10, 47), 'Classroom')
        self.assertEqual(attendance.minutes, 588)

    def test_should_get_correct_minutes_in_same_hour(self):
        attendance = Attendance(1, time(13, 5), time(13, 35), 'Classroom')
        self.assertEqual(attendance.minutes, 30)
