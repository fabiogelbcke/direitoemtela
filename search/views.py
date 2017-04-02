from django.shortcuts import render, redirect
from django.db.models import Q
from videos.models import Video, Tag
from django.views.generic import ListView

class SearchResultsView(ListView):
    model = Video
    paginate_by = 15
    context_object_name = 'videos'
    template_name = 'search-results.djhtml'

    def get_queryset(self):
        query = self.kwargs['query']
        if query == 'Todos os Videos':
            return Video.objects.all()
        tags = Tag.objects.filter(name__icontains=query)
        qs = Video.objects.filter(Q(title__icontains=query)
                                    | Q(description__icontains=query)
                                    | Q(tags__in=tags)).distinct()
        return qs

    def get_context_data(self, **kwargs):
        #qs = kwargs['object_list']
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['query'] = self.kwargs['query']
        context['total_videos'] = self.object_list.count()
        context['starting_index'] = (context['page_obj'].number - 1) * 15
        return context
# Create your views here.

def get_search_page(request):
    query = request.GET.get('query', 'Todos os Videos')
    if not query:
        query = 'Todos os Videos'
    return redirect('search_results_page', query=query)
