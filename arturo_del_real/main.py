import os
import sys
from datetime import time
from typing import List

from result import Result, Err, Ok

from utils import validate_time


class Attendance:
    MINUTES_TO_CONSIDER = 5

    def __init__(self, day: int, init_hour: time,
                 end_hour: time, classroom: str):
        self.day = day
        self.init_hour = init_hour
        self.end_hour = end_hour
        self.classroom = classroom

    def consider(self) -> bool:
        return self.minutes >= self.MINUTES_TO_CONSIDER

    @property
    def minutes(self) -> int:
        """get the minutes present in one attendance"""
        hour_difference = self.end_hour.hour - self.init_hour.hour
        minute_difference = self.end_hour.minute - self.init_hour.minute
        return hour_difference * 60 + minute_difference

    def __eq__(self, other):
        fields = ['day', 'init_hour', 'end_hour', 'classroom']
        if isinstance(other, Attendance):
            return all(
                map(
                    lambda field: getattr(self, field) == getattr(other,
                                                                  field),
                    fields
                )
            )
        return False


class Student:
    def __init__(self, name: str):
        self.name = name
        self.attendances = {}

    def add_data(self, data: List[str]) -> Result:
        """add one attendance if data is correct"""
        cleaned_data = self.__clean_data(data)
        if cleaned_data.is_err():
            return cleaned_data
        self.__add_data(*cleaned_data.ok())

    def __add_data(self, day: int, init_hour: time,
                   end_hour: time, classroom: str):
        new_attendance = Attendance(day, init_hour, end_hour, classroom)
        if not new_attendance.consider():
            return
        if day in self.attendances:
            self.attendances[day].append(new_attendance)
        else:
            self.attendances[day] = [new_attendance]

    @property
    def total_minutes(self):
        """get the total minutes of the week"""
        return sum(
            sum(
                attendance.minutes for attendance in attendances
            ) for attendances in self.attendances.values()
        )

    @property
    def days_present(self):
        """get the days of the week that the student is present"""
        return len(self.attendances)

    def get_resume(self):
        """get the requested resume"""
        days = self.days_present
        days_data = ''
        if days > 1:
            days_data = f' in {days} days'
        elif days == 1:
            days_data = f' in {days} day'
        return f'{self.name}: {self.total_minutes} ' \
               f'minutes{days_data}'

    @staticmethod
    def __clean_data(data: List[str]) -> Result:
        """validate the data to create a new attendance to the student"""
        if len(data) < 4:
            return Err('Missing data')
        day = data[0]
        if not day.isnumeric():
            return Err('Day must be numeric')
        day = int(day)
        if not 1 <= day <= 7:
            return Err('Day must be between 1 and 7')
        init_hour = validate_time(data[1])
        end_hour = validate_time(data[2])
        if init_hour.is_err():
            return Err('Invalid init date')
        if end_hour.is_err():
            return Err('Invalid end date')
        init_hour = init_hour.ok()
        end_hour = end_hour.ok()
        if end_hour < init_hour:
            return Err('Init date must be earlier than end date')
        return Ok((day, init_hour, end_hour, data[3]))

    def __eq__(self, other):
        fields = ['name', 'attendances']
        if isinstance(other, Student):
            return all(
                map(
                    lambda field: getattr(self, field) == getattr(other,
                                                                  field),
                    fields
                )
            )
        return False


class University:
    valid_commands = ['student', 'presence']

    def __init__(self):
        self.students = {}

    def _read_file(self, file_path: str) -> Result:
        if not os.path.exists(file_path) and os.path.isfile(file_path):
            return Err('The input file is invalid')
        commands = []
        with open(file_path) as infile:
            for line in infile:
                new_command = line.strip().split(' ')
                if new_command[0].lower() in self.valid_commands:
                    commands.append(new_command)
        return Ok(commands)

    def add_data_from_file(self, file_path: str) -> Result:
        """add students data based on a file"""
        commands_result = self._read_file(file_path)
        if commands_result.is_err():
            return commands_result
        commands = commands_result.ok()
        # add students first, so order in commands doesn't matter
        self.__add_students_from_commands(commands)
        self.__add_data_for_students_from_commands(commands)
        return Ok()

    def add_student(self, name: str):
        """add a new student if not exist. Should reuse"""
        if name not in self.students:
            self.students[name] = Student(name)

    def add_data_for_student(self, name: str, data: List[str]):
        """add student data if exists. Should reuse"""
        if name in self.students:
            self.students[name].add_data(data)

    def get_resume(self):
        """get the requested resume"""
        sorted_students = sorted(
            self.students.values(),
            key=lambda x: -x.total_minutes
        )
        return '\n'.join(map(lambda x: x.get_resume(), sorted_students))

    def __add_students_from_commands(self, commands: List):
        for command in commands:
            if command[0].lower() == 'student' and len(command) > 1:
                self.add_student(command[1])

    def __add_data_for_students_from_commands(self, commands: List):
        for command in commands:
            if command[0].lower() == 'presence' and len(command) > 1:
                self.add_data_for_student(command[1], command[2:])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Must provide an input file')
        sys.exit(1)
    university = University()
    valid = university.add_data_from_file('files/test01.txt')
    if valid.is_err():
        print(valid.err())
        sys.exit(1)
    print(university.get_resume())
