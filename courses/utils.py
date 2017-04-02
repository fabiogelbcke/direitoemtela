from .models import (Course, UserItemRelationship,
                     UserCourseRelationship, CourseItem)
from users.models import MyUser

def register_to_course(user_id, course_id):
    course = Course.objects.get(id=course_id)
    user = MyUser.objects.get(id=user_id)
    UserCourseRelationship.objects.create(
        user=user,
        course=course
    )
    for item in course.items.all():
        UserItemRelationship.objects.create(
            user=user,
            course_item=item
    )
