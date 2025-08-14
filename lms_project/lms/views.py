# lms/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from lms.dto.course_dto import CourseDTO
from lms.serializers import CourseSerializer
from .unit_of_work import UnitOfWork
from lms.services.student_service import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student,
    delete_student
)

# lms/views.py
from lms.services.course_service import (
    create_course,
    get_all_courses,
    get_course_by_id,
    update_course,
    delete_course
)

# lms/views.py
from .serializers import UserSerializer

from .serializers import UserWithCoursesSerializer

class CourseCreateView(APIView):
    def get(self, request):
        courses = get_all_courses()  # Service method to fetch all courses
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            dto = CourseDTO(title=serializer.validated_data['title'], description=serializer.validated_data['description'])
            course = create_course(dto)
            return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    def get(self, request, pk):
        course = get_course_by_id(pk)
        if not course:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        course = get_course_by_id(pk)
        if not course:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data, partial=False)
        if serializer.is_valid():
            dto = CourseDTO(
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description']
            )
            updated_course = update_course(pk, dto)
            return Response(CourseSerializer(updated_course).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if delete_course(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)


class CreateStudentAPIView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        course_ids = data.get("course_ids", [])
        print(data)
        try:
            with UnitOfWork() as uow:
                student = uow.create_student_with_courses(username, email, password, course_ids)
            
            return Response({
                "id": student.id,
                "username": student.user.username,
                "enrolled_courses": [c.title for c in student.enrolled_courses.all()]
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StudentListView(APIView):
    def get(self, request):
        with UnitOfWork() as uow:
            students = uow.students.list()
        serializer = UserWithCoursesSerializer([s.user for s in students], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        student = create_student(
            username=data['username'],
            email=data.get('email', ''),
            password=data['password'],
            course_ids=data.get('course_ids', [])
        )
        serializer = UserSerializer(student.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StudentDetailView(APIView):
    def get(self, request, pk):
        student = get_student_by_id(pk)
        if not student:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(student.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        data = request.data
        student = update_student(
            pk,
            username=data.get('username'),
            email=data.get('email'),
            course_ids=data.get('course_ids')
        )
        if not student:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(student.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        success = delete_student(pk)
        if not success:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)