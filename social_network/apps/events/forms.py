from django.forms import ModelForm, Textarea
from .models import Event



class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('event_title', 'event_text', 'event_image')
        widgets = {
            'event_text': Textarea(attrs={'rows': 3}),
        }
