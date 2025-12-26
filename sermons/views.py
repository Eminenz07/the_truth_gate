from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Sermon, Series, Topic

class SermonListView(ListView):
    model = Sermon
    template_name = 'sermons/sermon_list.html'
    context_object_name = 'sermons'
    paginate_by = 12

    def get_queryset(self):
        queryset = Sermon.objects.filter(status='published')
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort', 'latest') # Default to latest unless overridden

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(speaker__name__icontains=query) |
                Q(series__title__icontains=query)
            )

        # Topic Filtering
        topic_slug = self.request.GET.get('topic')
        if topic_slug:
            queryset = queryset.filter(topics__slug=topic_slug)

        # Sorting Logic
        if sort_by == 'oldest':
            queryset = queryset.order_by('date_preached')
        elif sort_by == 'a-z':
            queryset = queryset.order_by('title')
        elif sort_by == 'z-a':
            queryset = queryset.order_by('-title')
        else: # latest
            queryset = queryset.order_by('-date_preached')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get('sort', 'all') 
        context['current_sort'] = sort_by
        
        # Only fetch topics structure if we are in the 'all' (grouped) view
        if sort_by == 'all':
            from django.db.models import Prefetch
            # Fetch topics that actually have published sermons
            context['grouped_topics'] = Topic.objects.filter(
                sermon__status='published'
            ).distinct().prefetch_related(
                Prefetch('sermon_set', 
                         queryset=Sermon.objects.filter(status='published').order_by('-date_preached')[:4],
                         to_attr='latest_sermons')
            )
            
        return context

class SermonDetailView(DetailView):
    model = Sermon
    template_name = 'sermons/sermon_detail.html'
    context_object_name = 'sermon'

    def get_queryset(self):
        return Sermon.objects.filter(status='published')
