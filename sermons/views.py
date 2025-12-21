from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Sermon, Series

class SermonListView(ListView):
    model = Sermon
    template_name = 'sermons/sermon_list.html'
    context_object_name = 'sermons'
    paginate_by = 12

    def get_queryset(self):
        queryset = Sermon.objects.filter(status='published')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(speaker__name__icontains=query) |
                Q(series__title__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series_list'] = Series.objects.all()[:5]
        return context

class SermonDetailView(DetailView):
    model = Sermon
    template_name = 'sermons/sermon_detail.html'
    context_object_name = 'sermon'

    def get_queryset(self):
        return Sermon.objects.filter(status='published')
