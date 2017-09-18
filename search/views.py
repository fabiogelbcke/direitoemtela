# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from videos.models import Video, Tag
from courses.models import Course, CourseTopic

class VideoSearchResultsView(ListView):
    model = Video
    paginate_by = 15
    context_object_name = 'videos'
    template_name = 'video-search-results.djhtml'

    def get_queryset(self):
        query = self.kwargs['query']
        print 'query:'
        print query
        if query == u'Todos os Cursos e Vídeos':
            return Video.objects.all()
        tags = Tag.objects.filter(name__icontains=query)
        qs = Video.objects.filter(Q(title__icontains=query)
                                    | Q(description__icontains=query)
                                    | Q(tags__in=tags)).distinct()
        print qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(VideoSearchResultsView, self).get_context_data(**kwargs)
        query = self.kwargs['query']
        if query == u'Todos os Cursos e Vídeos':
            query = u'Todos os Vídeos'
        context['query'] = query
        context['total_videos'] = self.object_list.count()
        context['starting_index'] = (context['page_obj'].number - 1) * 15
        return context


class CourseSearchResultsView(ListView):
    model = Course
    paginate_by = 15
    context_object_name = 'courses'
    template_name = 'course-search-results.djhtml'

    def get_queryset(self):
        query = self.kwargs['query']
        print query
        if query == u'Todos os Cursos e Vídeos':
            return Course.objects.all()
        topics = CourseTopic.objects.filter(text__icontains=query)
        qs = Course.objects.filter(Q(name__icontains=query)
                                    | Q(description__icontains=query)
                                    | Q(topics__in=topics)).distinct()
        print qs
        return qs

    def get_context_data(self, **kwargs):
        #qs = kwargs['object_list']
        context = super(CourseSearchResultsView, self).get_context_data(**kwargs)
        query = self.kwargs['query']
        if query == u'Todos os Cursos e Vídeos':
            query = u'Todos os Cursos'
        context['query'] = query
        context['total_courses'] = self.object_list.count()
        context['starting_index'] = (context['page_obj'].number - 1) * 15
        return context


class SearchResultsView(TemplateView):
    template_name = 'search-results.djhtml'

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        query = self.kwargs['query']
        tags = Tag.objects.filter(name__icontains=query)
        if unicode(query) == u'Todos os Cursos e Vídeos':
            videos = Video.objects.all()
            courses = Course.objects.all()
        else:
            videos = Video.objects.filter(Q(title__icontains=query)
                                          | Q(description__icontains=query)
                                          | Q(tags__in=tags)).distinct()
            courses = Course.objects.filter(Q(name__icontains=query)
                                            | Q(description__icontains=query)).distinct()
            #| Q(tags__in=tags)).distinct()
        context['query'] = query
        context['videos'] = videos[:3]
        context['total_videos'] = videos.count()
        context['courses'] = courses[:3]
        context['total_courses'] = courses.count()
        return context


def get_search_page(request):
    query = request.GET.get('query', 'Todos os Cursos e Vídeos')
    if not query:
            query = 'Todos os Cursos e Vídeos'
    user = request.user
    if user.is_authenticated() and user.is_beta:
        return redirect('search_results_page',
                        query=query)
    else:
        return redirect('video_search_results_page',
                        query=query)
