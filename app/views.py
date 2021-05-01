from django.shortcuts import render
from .forms import Caseform, Eventform
from django.http import HttpResponse, HttpResponseRedirect
from .models import Case, Event
from datetime import datetime, timedelta, date

# Create your views here.

def Base(request):
    template_name = 'base.html'

    return render(request, template_name)

def Showcase(request):
    form = Caseform()

    return render(request, 'addcase.html', {'form':form})

def Showevent(request):
    #This function first stores the Case data and 
    #then renders the add event form
    if request.method == 'POST':
        form = Caseform(request.POST)       
        if form.is_valid():
            form.save()  

    form1 = Eventform()      
    return render(request, 'addevent.html', {'form':form1})

def Addevent(request):
    #This function first stores the previously entered even 
    #and then renders the add event form again.

    form = Eventform(request.POST)       
    if form.is_valid():
        min_date = Case.objects.get(id=form.data['case']).date_of_onset - timedelta(14)
        max_date = Case.objects.get(id=form.data['case']).date_of_confirmation 
        e_date = datetime.strptime(form.data['date'], '%Y-%m-%d').date()
        if e_date < min_date :
            return render(request, 'dateerror.html', {'errormessage':"The date of Event is before the 14th day, Do not add this event or change date"})
        
        if e_date > max_date :
            return render(request, 'dateerror.html', {'errormessage':"The date of Event is after the date of confirmation, Do   not add this event or change date"})

        form.save()        
    form1 = Eventform()      
    return render(request, 'addevent.html', {'form':form1})
