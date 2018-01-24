# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils import timezone

from .models import (Course, UserItemRelationship,
                     UserCourseRelationship, CourseItem,
                     Certificate)

from coursetests.models import UserQuestionRelationship
from users.models import MyUser

from io import BytesIO


def send_registration_confirmation_email(user, course):
    template = loader.get_template('email-course-registration.djhtml')
    content = template.render({
        'user': user,
        'course': course
    })
    subject = 'Inscrição no Minicurso Confirmado!'
    email = user.email
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email='Equipe Direito em Tela <contato@direitoemtela.com.br>',
        to=[email,]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send()
    return True


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
    send_registration_confirmation_email(user, course)
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


def send_course_completed_email(course_rel, user):
    course = course_rel.course
    if course_rel.passed == True:
        template = loader.get_template('email-course-passed.djhtml')
    else:
        template = loader.get_template('email-course-failed.djhtml')
    content = template.render({
        'user': user,
        'course': course
    })
    subject = 'Curso de ' + course.name + ' Completo!'
    email = user.email
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email='Equipe Direito em Tela <contato@direitoemtela.com.br>',
        to=[email,]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send()
    return True


def complete_course(course_rel, user):
    course_rel.passed = course_rel.percentage() >= course_rel.passing_grade
    course_rel.completed = True
    course_rel.completion_date = timezone.now()
    course_rel.certificate = create_certificate(course_rel)
    course_rel.save()
    user.course_hours += course_rel.course.hours
    user.save()
    send_course_completed_email(course_rel, user)
    return course_rel
