from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import requires_csrf_token
from .models import (Course, CourseItem, UserCourseRelationship,
                     UserItemRelationship, Certificate)
from .utils import create_certificate, render_to_pdf
from coursetests.models import UserQuestionRelationship
from .decorators import is_registered_to_course
from easy_pdf.views import PDFTemplateResponseMixin

#get the range of items that show up on the progress bar at the
#top of the page while doing the course
def get_items_range(pos, total_items):
    min_pos = pos - 8
    max_pos = pos + 7
    if min_pos < 1:
        max_pos = max_pos - min_pos + 1
        min_pos = 1
    if max_pos > total_items:
        min_pos -= max_pos - total_items
        min_pos = max(1, min_pos)
        max_pos = total_items
    return min_pos, max_pos


class CourseView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'course-page.djhtml'
    slug_field = 'id'
    pk_url_kwarg = "course_id"

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        user = self.request.user
        course = self.object
        if user.is_authenticated():
            if hasattr(user, 'billing_info'):
                context['billing_info'] = user.billing_info
            if course.is_registered(user):
                context['course_rel'] = course.course_rels.get(user=user)
        context['course_items'] = course.items.all().order_by('position')
        return context


@method_decorator(is_registered_to_course, 'dispatch')
class CourseProgressView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'course-progress.djhtml'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super(CourseProgressView, self).get_context_data(**kwargs)
        user = self.request.user
        course = self.object
        item_rels = UserItemRelationship.objects.filter(
            user=user,
            course_item__course=course
        ).order_by('course_item__position')
        course_rel = UserCourseRelationship.objects.get(
            user=user,
            course=course
        )
        videos = item_rels.filter(
            course_item__video__isnull=False
        )
        readings = item_rels.filter(
            course_item__reading__isnull=False
        )
        tests = item_rels.filter(
            course_item__test__isnull=False
        )
        completed = bool(self.request.GET.get('completed', False))
        context['item_rels'] = item_rels
        context['course_rel'] = course_rel
        context['videos_total'] = videos.count()
        context['videos_done'] = videos.filter(done=True).count()
        context['readings_total'] = readings.count()
        context['readings_done'] = readings.filter(done=True).count()
        context['tests_total'] = tests.count()
        context['tests_done'] = tests.filter(done=True).count()
        context['completed'] = completed
        return context
        

@method_decorator(is_registered_to_course, 'dispatch')
@method_decorator(requires_csrf_token, name='dispatch')
class CourseItemView(LoginRequiredMixin, DetailView):
    model = CourseItem
    context_object_name = 'course_item'
    template_name = 'course-video.djhtml'

    
    def get_object(self):
        position = self.kwargs['position']
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        total_items = course.items.all().count()
        pos = min(int(total_items), int(position))
        return CourseItem.objects.get(position=pos, course=course)

    
    def dispatch(self, request, *args, **kwargs):
        course = self.get_object().course
        user = request.user
        course_rel = UserCourseRelationship.objects.get(
                    course=course,
                    user=user
        )
        if (course_rel.questions_answered == course_rel.total_questions
            and course_rel.completed == False):
            course_rel.passed = course_rel.percentage() >= course_rel.passing_grade
            course_rel.completed = True
            course_rel.completion_date = timezone.now()
            course_rel.certificate = create_certificate(course_rel)
            course_rel.save()
            user.course_hours += course.hours
            user.save()
            response = redirect('course_progress', course_id=course.id)
            response['Location'] += '?completed=true'
            return response
        else:
            return super(CourseItemView, self).dispatch(request, *args, **kwargs)

            
    def get_test_context(self, context, user_course_rel, **kwargs):
        test = self.object.test
        user = self.request.user
        if 'question_no' in self.kwargs:
            question_no = int(self.kwargs['question_no'])
        else:
            question_no = UserQuestionRelationship.objects.filter(
                user=user,
                question__test=test,
                answered=True
            ).count() + 1
        if question_no <= test.questions.all().count():
            context['question'] = test.questions.all()[question_no - 1]
        else:
            all_questions = UserQuestionRelationship.objects.filter(
                user=user,
                question__test=test,
            )
            correctly_answered = all_questions.filter(
                answered_correctly=True
            ).count()
            test_percentage = int(100.0*correctly_answered/all_questions.count())
            course_percentage = user_course_rel.percentage
            context['test_percentage'] = test_percentage
            context['course_percentage'] = course_percentage
        context['question_no'] = question_no
        return context

    def get_video_context(self, context, **kwargs):
        video = self.object.video
        complementary_materials = video.complementary_materials.all()
        context['complementary_links'] = [m for m in complementary_materials if m.is_link()]
        context['complementary_files'] = [m for m in complementary_materials if m.is_file()]
        print len(context['complementary_links'])
        print len(context['complementary_files'])
        return context

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CourseItemView, self).get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['course_id'])
        total_items = CourseItem.objects.filter(course=course).count()
        pos = int(self.kwargs['position'])
        min_pos, max_pos = get_items_range(pos, total_items)
        user_item_rels = UserItemRelationship.objects.filter(
            user=user,
            course_item__course=course,
            course_item__position__gte=min_pos,
            course_item__position__lte=max_pos
        ).order_by('course_item__position')
        course_rel = UserCourseRelationship.objects.get(
                    course=course,
                    user=user
        )
        context['user_item_rels'] = user_item_rels
        context['course'] = course
        context['total_steps'] = course.items.all().count()
        if self.object.type() == 'test':
            return self.get_test_context(context, course_rel, **kwargs)
        if self.object.type() == 'video':
            return self.get_video_context(context, **kwargs)
        return context

    
@login_required
def dashboard_courses(request):
    user = request.user
    completed_courses_rels = UserCourseRelationship.objects.filter(
        user=user,
        completed=True
    )
    ongoing_courses_rels = UserCourseRelationship.objects.filter(
        user=user,
        completed=False,
    )
    template = loader.get_template('dashboard.djhtml')
    return HttpResponse(template.render({
        'completed_courses_rels': completed_courses_rels,
        'ongoing_courses_rels': ongoing_courses_rels,
        }, request))


class CertificateView(DetailView):
    model = Certificate
    pk_url_kwarg = 'identifier'
    slug_field = 'identifier'
    context_object_name = 'certificate'
    template_name = 'course-certificate.djhtml'

    def get_context_data(self, **kwargs):
        context = super(CertificateView, self).get_context_data(**kwargs)
        context['website_url'] = settings.WEBSITE_URL[:-1]
        return context


class CertificatePrint(DetailView):
    model = Certificate
    pk_url_kwarg = 'identifier'
    slug_field = 'identifier'
    context_object_name = 'certificate'
    template_name = 'certificate-for-print.djhtml'

    def get_context_data(self, **kwargs):
        context = super(CertificatePrint, self).get_context_data(**kwargs)
        return context
    
