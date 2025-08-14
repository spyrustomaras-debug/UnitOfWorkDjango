from lms.models import Course

class CourseRepository:
    def get_by_id(self, id: int):
        return Course.objects.get(id=id)

    def list(self):
        return Course.objects.all()

    def add(self, course: Course):
        course.save()
        return course

    def delete(self, course: Course):
        course.delete()
