from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Course, CourseItem


class CourseView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'course-page.djhtml'
    slug_field = 'id'

    
class CourseItemView(DetailView):
    model = CourseItem
    context_object_name = 'course_item'
    template_name = 'course-video.djhtml'

    def get_object(self):
        pos = self.kwargs['position']
        course = Course.objects.get(id=self.kwargs['course_id'])
        return CourseItem.objects.get(position=pos, course=course)

    def get_context_data(self, **kwargs):
        context = super(CourseItemView, self).get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['course_id'])
