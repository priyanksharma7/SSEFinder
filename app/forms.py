from django.forms import ModelForm, DateInput, ModelChoiceField, ModelMultipleChoiceField, Select   
from .models import Event,Case


class DateInput(DateInput):
    input_type = 'date'

class Caseform(ModelForm):
    class Meta:
        widgets = {'date_of_birth': DateInput(), 'date_of_onset': DateInput(), 'date_of_confirmation': DateInput()}
        model = Case
        fields = '__all__'

class Eventform(ModelForm):
    class Meta:     
        widgets = {'date': DateInput()}   
        model = Event        
        fields = ['venue_name', 'venue_location', 'date', 'description']
