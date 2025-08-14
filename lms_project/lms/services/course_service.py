from lms.models import Course

def get_all_courses():
    return Course.objects.all()

def get_course_by_id(course_id):
    try:
        return Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return None

def create_course(dto):
    course = Course.objects.create(
        title=dto.title,
        description=dto.description
    )
    return course

def update_course(course_id, dto):
    course = get_course_by_id(course_id)
    if not course:
        return None
    course.title = dto.title
    course.description = dto.description
    course.save()
    return course

def delete_course(course_id):
    course = get_course_by_id(course_id)
    if not course:
        return False
    course.delete()
    return True
