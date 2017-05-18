from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from videos.models import Video
from .models import Category
from hitcount.views import HitCountDetailView



class CategoryView(ListView):
    model = Video
    paginate_by = 15
    context_object_name = 'videos'
    template_name = 'category-page.html'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        qs = category.videos.all().order_by('videocategory__position')
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
        return Category.objects.filter(hidden=False)

class CategoryVideoView(HitCountDetailView):
    template_name = 'video-page.djhtml'
    context_object_name = 'video'
    model = Video
    count_hit = True

    def get_object(self):
        category_id = int(self.kwargs['category_id'])
        category = get_object_or_404(Category, id=category_id)
        video_index = int(self.kwargs['video_index'])
        if not 0 < video_index <= category.videos.all().count():
            raise Http404
        try:
            video = category.videos.get(videocategory__position = video_index)
        except ObjectDoesNotExist:
            raise Http404
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
        suggestions = category_videos.filter(videocategory__position__gt=video_index)[:16]
        context['category'] = category
        context['video_index'] = video_index
        context['suggestions'] = suggestions
        context['videos_in_category'] = category_videos.count()
        context['skip_automatically'] = video_index < category_videos.count()
        context['video_url'] = settings.WEBSITE_URL[:-1]
        context['video_url'] += reverse('category_video', kwargs={'category_id': category_id, 'video_index': video_index})
        return context
