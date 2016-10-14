from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from categories.models import Category

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['featured_categories'] = Category.objects.filter(featured=True)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('under_construction')
        else:
            return super(IndexView, self).dispatch(request, *args, **kwargs)

