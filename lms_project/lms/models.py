# lms/models.py
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    students = models.ManyToManyField(User, related_name="courses")

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    enrolled_courses = models.ManyToManyField(Course, related_name="enrolled_students")

    def __str__(self):
        return f"Student: {self.user.username}"
