# lms/serializers.py

from rest_framework import serializers
from lms.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description']


# lms/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserWithCoursesSerializer(serializers.ModelSerializer):
    enrolled_courses = CourseSerializer(source='student_profile.enrolled_courses', many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'enrolled_courses']

