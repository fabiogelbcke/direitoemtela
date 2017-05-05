from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import (Course, UserItemRelationship,
                     UserCourseRelationship, CourseItem)
from coursetests.models import UserQuestionRelationship
from users.models import MyUser


def register_to_course(user_id, course_id):
    course = Course.objects.get(id=course_id)
    user = MyUser.objects.get(id=user_id)
    if UserCourseRelationship.objects.filter(
            user=user,
            course=course
    ).exists():
        return False
    UserCourseRelationship.objects.create(
        user=user,
        course=course
    )
    for item in course.items.all():
        UserItemRelationship.objects.create(
            user=user,
            course_item=item
        )
        if item.type() == 'test':
            for question in item.test.questions.all():
                UserQuestionRelationship.objects.create(
                    user=user,
                    question=question
                )

@login_required
def set_item_done(request, item_id):
    u_item_rel = UserItemRelationship.objects.get(
        course_item__id=item_id,
        user=request.user
    )
    u_item_rel.done=True
    u_item_rel.save()
    return HttpResponse('good!')
