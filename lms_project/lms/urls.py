# lms/urls.py

from django.urls import path
from lms.views import CourseCreateView, CourseDetailView
from .views import CreateStudentAPIView
from lms.views import StudentListView, StudentDetailView

urlpatterns = [
    path('courses/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path("students/create/", CreateStudentAPIView.as_view(), name="create-student"),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
]
