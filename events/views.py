from django.views.generic import ListView
from django.utils import timezone
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        # Show future events first, exclude completed ones
        return Event.objects.filter(is_completed=False).order_by('-start_time')
