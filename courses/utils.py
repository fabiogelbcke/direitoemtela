from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import (Course, UserItemRelationship,
                     UserCourseRelationship, CourseItem,
                     Certificate)
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
        course=course,
        total_questions=course.total_questions
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
                    question=question,
                )
    return True

def unregister_to_course(user_id, course_id):
    course = Course.objects.get(id=course_id)
    user = MyUser.objects.get(id=user_id)
    UserCourseRelationship.objects.filter(
        user=user,
        course=course,
        total_questions=course.total_questions
    ).delete()
    for item in course.items.all():
        UserItemRelationship.objects.filter(
            user=user,
            course_item=item
        ).delete()
        if item.type() == 'test':
            for question in item.test.questions.all():
                UserQuestionRelationship.objects.filter(
                    user=user,
                    question=question,
                ).delete()
    return True

@login_required
def set_item_done(request, item_id):
    course_item = CourseItem.objects.get(id=item_id)
    u_item_rel = UserItemRelationship.objects.get(
        course_item=course_item,
        user=request.user
    )
    u_item_rel.done=True
    u_item_rel.save()
    user_course_rel = UserCourseRelationship.objects.get(
        course=course_item.course,
        user=user
    )
    user_course_rel.last_accessed_item = course_item
    user_course_rel.save()
    return HttpResponse('good!')


def create_certificate(course_rel):
    course = course_rel.course
    certificate = Certificate.objects.create(
        user=course_rel.user,
        course_name=course.name,
        course_hours=course.hours,
        percentage=course_rel.percentage()
    )
    return certificate
