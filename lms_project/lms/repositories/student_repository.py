# lms/repositories/student_repository.py
from django.contrib.auth.models import User
from lms.models import Student

class StudentRepository:
    def get_by_id(self, id: int):
        return Student.objects.get(id=id)

    def list(self):
        return Student.objects.all()

    def add(self, student: Student):
        student.save()
        return student

    def delete(self, student: Student):
        student.delete()
