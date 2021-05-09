from django.forms import ModelForm, DateInput
from .models import Case, Event

class CaseForm(ModelForm):
    class Meta:
        model = Case
        fields = '__all__'
        widgets = {
                'date_of_birth': DateInput(attrs={'class': 'datepicker'}),
                'date_of_onset': DateInput(attrs={'class': 'datepicker'}),
                'date_of_confirmation': DateInput(attrs={'class': 'datepicker'}),
        }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['venue_name', 'venue_location', 'date', 'description']
        widgets = {
                'date': DateInput(attrs={'class': 'datepicker'}),
        }