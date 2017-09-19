from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template.loader import get_template

from .models import (Course, UserItemRelationship,
                     UserCourseRelationship, CourseItem,
                     Certificate)

from coursetests.models import UserQuestionRelationship
from users.models import MyUser

from io import BytesIO
from xhtml2pdf import pisa


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

def unregister_from_course(user_id, course_id):
    course = Course.objects.get(id=course_id)
    user = MyUser.objects.get(id=user_id)
    UserCourseRelationship.objects.filter(
        user=user,
        course=course
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


def admin_register_to_course(request, course_id):
    if (request.user.is_authenticated
        and request.user.is_admin):
        register_to_course(request.user.id, course_id)
        return redirect('course_page', course_id=course_id)
    else:
        raise Http404()

    
def admin_unregister_from_course(request, course_id):
    if (request.user.is_authenticated
        and request.user.is_admin):
        unregister_from_course(request.user.id, course_id)
        return redirect('course_page', course_id=course_id)
    else:
        raise Http404()
    

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
        user=request.user
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


def render_to_pdf(template_src, context={}):
    template = get_template(template_src)
    html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
