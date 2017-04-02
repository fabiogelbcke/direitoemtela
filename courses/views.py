from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Course, CourseItem, UserCourseRelationship, UserItemRelationship
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.mixins import LoginRequiredMixin


class CourseView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'course-page.djhtml'
    slug_field = 'id'

    
class CourseItemView(LoginRequiredMixin, DetailView):
    model = CourseItem
    context_object_name = 'course_item'
    template_name = 'course-video.djhtml'

    def get_object(self):
        pos = self.kwargs['position']
        course = Course.objects.get(id=self.kwargs['course_id'])
        return CourseItem.objects.get(position=pos, course=course)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CourseItemView, self).get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['course_id'])
        total_items = CourseItem.objects.filter(course=course).count()
        pos = int(self.kwargs['position'])
        min_pos = pos - 8
        max_pos = pos + 7
        print 'min {} max {}'.format(min_pos, max_pos)
        if min_pos < 1:
            max_pos = max_pos - min_pos + 1
            min_pos = 1
        print 'min {} max {}'.format(min_pos, max_pos)
        if max_pos > total_items:
            min_pos -= max_pos - total_items
            min_pos = max(1, min_pos)
            max_pos = total_items
        print 'min {} max {}'.format(min_pos, max_pos)

        user_item_rels = UserItemRelationship.objects.filter(
            user=user,
            course_item__course=course,
            course_item__position__gte=min_pos,
            course_item__position__lte=max_pos
        ).order_by('course_item__position')
        context['user_item_rels'] = user_item_rels
        context['course'] = course
        if self.object.type() == 'test':
            if 'question_no' in self.kwargs:
                question_no = int(self.kwargs['question_no'])
            else:
                question_no = 1
            context['question'] = self.object.test.questions.all()[question_no - 1]
            context['question_no'] = question_no
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
    
