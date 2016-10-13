from django.shortcuts import render
from django.views.generic import TemplateView
from categories.models import Category

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['featured_categories'] = Category.objects.filter(featured=True)
        return context
