# lms/dto/course_dto.py

from dataclasses import dataclass

@dataclass
class CourseDTO:
    title: str
    description: str
