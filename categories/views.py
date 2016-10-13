from django.shortcuts import render
from django.views.generic import ListView
from videos.models import Video
from .models import Category

class CategoryView(ListView):
    model = Video
    paginate_by = 15
    context_object_name = 'videos'
    template_name = 'category-page.html'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = Category.objects.get(id=category_id)
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
