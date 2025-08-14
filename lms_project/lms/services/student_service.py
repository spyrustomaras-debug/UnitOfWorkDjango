# lms/services/student_service.py
from lms.unit_of_work import UnitOfWork

def get_all_students():
    with UnitOfWork() as uow:
        return uow.students.list()

def get_student_by_id(student_id):
    with UnitOfWork() as uow:
        try:
            return uow.students.get_by_id(student_id)
        except Exception:
            return None

def create_student(username, email, password, course_ids=[]):
    with UnitOfWork() as uow:
        return uow.create_student_with_courses(username, email, password, course_ids)

def update_student(student_id, username=None, email=None, course_ids=None):
    with UnitOfWork() as uow:
        student = uow.students.get_by_id(student_id)
        if not student:
            return None
        if username:
            student.user.username = username
        if email:
            student.user.email = email
        if course_ids is not None:
            courses = uow.courses.list().filter(id__in=course_ids)
            student.enrolled_courses.set(courses)
        student.user.save()
        return uow.students.add(student)

def delete_student(student_id):
    with UnitOfWork() as uow:
        student = uow.students.get_by_id(student_id)
        if not student:
            return False
        uow.students.delete(student)
        return True
