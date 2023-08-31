from unittest import TestCase
from unittest.mock import patch

from result import Ok

from main import University, Student


class UniversityTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_content = [
            ['Student', 'Marco'],
            ['Student', 'David'],
            ['Student', 'Fran'],
            ['Presence', 'Marco', '1', '09:02', '10:17', 'R100'],
            ['Presence', 'Marco', '3', '10:58', '12:05', 'R205'],
            ['Presence', 'David', '5', '14:02', '15:46', 'F505'],
            ['Presence', 'Fran', '2', '11:02', '14:06', 'F505']
        ]

    def setUp(self):
        self.university = University()
        self.basic_presence = [
            'Presence',
            'Fran',
            '1',
            '00:00',
            '00:10',
            'Classroom'
        ]

    @patch('main.University._read_file')
    def test_should_properly_add_data_from_file(self, mocked_commands):
        mocked_commands.return_value = Ok([
            ['Student', 'Fran'],
            self.basic_presence,
        ])
        valid = self.university.add_data_from_file('filepath')
        self.assertTrue(valid.is_ok())

        student = Student('Fran')
        student.add_data(self.basic_presence[2:])

        expected_students = {
            'Fran': student
        }
        self.assertEqual(expected_students, self.university.students)

    def test_should_add_student(self):
        self.university.add_student('Fran')
        expected_students = {
            'Fran': Student('Fran')
        }
        self.assertEqual(expected_students, self.university.students)

    def test_should_add_data_for_student(self):
        self.university.add_student('Fran')
        self.university.add_data_for_student('Fran', self.basic_presence[2:])
        student = Student('Fran')
        student.add_data(self.basic_presence[2:])

        expected_students = {
            'Fran': student
        }
        self.assertEqual(expected_students, self.university.students)

    @patch('main.University._read_file')
    def test_should_get_Resume(self, mocked_commands):
        mocked_commands.return_value = Ok(self.file_content)
        self.university.add_data_from_file('filepath')
        expected_resume = "Fran: 184 minutes in 1 day\n" \
                          "Marco: 142 minutes in 2 days\n" \
                          "David: 104 minutes in 1 day"
        self.assertEqual(self.university.get_resume(), expected_resume)
