from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from videos.models import Video
from .models import Category
from django.shortcuts import get_object_or_404
from django.http import Http404
from hitcount.views import HitCountDetailView


class CategoryView(ListView):
    model = Video
    paginate_by = 15
    context_object_name = 'videos'
    template_name = 'category-page.html'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        qs = category.videos.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        category = Category.objects.get(id=category_id)
        context['category'] = category
        context['total_videos'] = category.videos.all().count()
        context['starting_index'] = (context['page_obj'].number - 1) * 15
        return context
# Create your views here.

class CategoriesListView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()

class CategoryVideoView(HitCountDetailView):
    template_name = 'video-page.html'
    context_object_name = 'video'
    model = Video
    count_hit = True

    def get_object(self):
        category_id = int(self.kwargs['category_id'])
        category = get_object_or_404(Category, id=category_id)
        video_index = int(self.kwargs['video_index'])
        if not 0 < video_index <= category.videos.all().count():
            print -1
            print video_index
            print category.videos.all().count()
            raise Http404
        video = category.videos.all()[video_index - 1]
        return video

    def get_context_data(self, **kwargs):
        context = super(CategoryVideoView, self).get_context_data(**kwargs)
        category_id = int(self.kwargs['category_id'])
        category = get_object_or_404(Category, id=category_id)
        video_index = int(self.kwargs['video_index'])
        category_videos = category.videos.all()
        if not 0 < video_index <= category_videos.count():
            raise Http404
        #video suggestions: 15 videos after the current or videos left in
        #category after the current. whichever one is less
        suggestions = category_videos[video_index: video_index + 16]
        context['category'] = category
        context['video_index'] = video_index
        context['suggestions'] = suggestions
        context['videos_in_category'] = category_videos.count()
        return context
