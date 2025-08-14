from django.db import transaction
from lms.repositories.course_repository import CourseRepository
from lms.repositories.student_repository import StudentRepository
from django.contrib.auth.models import User  # <-- Import User
from .models import Student, Course         # import Student and Course

class UnitOfWork:
    def __init__(self):
        self.courses = CourseRepository()
        self.students = StudentRepository()


    def __enter__(self):
        self.txn = transaction.atomic()
        self.txn.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.txn.__exit__(exc_type, exc_val, exc_tb)

     # Create student and enroll in selected courses
    def create_student_with_courses(self, username, email, password, course_ids=[]):
        user = User.objects.create_user(username=username, email=email, password=password)
        student = Student.objects.create(user=user)
        
        courses = Course.objects.filter(id__in=course_ids)
        student.enrolled_courses.set(courses)
        student.save()
        return student