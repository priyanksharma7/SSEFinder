from django.shortcuts import render
from .forms import Caseform, Eventform
from .models import Case, Event
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def Home(request):
    template_name = 'home.html'
    return render(request, template_name)

@login_required
def Showcase(request):
    form = Caseform()
    return render(request, 'addcase.html', {'form':form})

@login_required
def Showevent(request):
    #This function first stores the Case data and 
    #then renders the add event form
    global wCase
    context = {}
    if request.method == 'POST':
        form = Caseform(request.POST)       
        if form.is_valid():
            wCase = form.save()              
    form1 = Eventform() 
    context['case']=wCase.patient_name 
    context['form'] = form1
    return render(request, 'addfirstevent.html', context)

@login_required
def Addevent(request):
    #This function first stores the previously entered even 
    #and then renders the add event form again.
    form = Eventform(request.POST)       
    if form.is_valid():
        min_date = wCase.date_of_onset - timedelta(14)
        max_date = wCase.date_of_confirmation 
        e_date = datetime.strptime(form.data['date'], '%Y-%m-%d').date()
        if e_date < min_date :
            return render(request, 'dateerror.html', {'errormessage':"The date of Event is before the 14th day, Do not add this event or change date"})
        
        elif e_date > max_date :
            return render(request, 'dateerror.html', {'errormessage':"The date of Event is after the date of confirmation, Do   not add this event or change date"})

        else:
            dForm = Event(case=wCase, venue_name=form.cleaned_data['venue_name'], venue_location=form.cleaned_data['venue_location'], date=form.cleaned_data['date'], description=form.cleaned_data['description'])
            dForm.save()   
    form1 = Eventform()      
    return render(request, 'addevent.html', {'form':form1, 'case':wCase.patient_name})

@login_required
def SearchCase(request):
    context={}
    if request.method == 'POST':        
        sCasenum=request.POST['sCasenum']
        if sCasenum.isdigit():
            dCase= Case.objects.filter(case_num=sCasenum).first() 
        else:
            context['valErr']= True
            context['num'] = sCasenum
            return render(request, 'search.html', context)

        if dCase == None:
            context['dne'] = True
            context['num'] = sCasenum
            return render(request, 'search.html', context)
        context['casedeets'] = dCase
        context['eList'] = dCase.event_set.all()
    return render(request, 'search.html', context)

@login_required
def SSE(request):
    template_name = 'sse.html'
    context = {}
    context['empty'] = False

    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')

        startdate = datetime.strptime(start, '%d/%m/%Y').date()
        enddate = datetime.strptime(end, '%d/%m/%Y').date()

        if startdate > enddate:
            context['error'] = "End Date should be after Start Date"

        else:
            context['data'] = {}
            context['range'] = [startdate, enddate]
            for e in Event.objects.all():
                if e.date >= startdate and e.date <= enddate:
                    event = (e.date, e.venue_name, e.venue_location, e.address, e.x_coordinate, e.y_coordinate)
                    if event not in context['data']:
                        context['data'][event] = []
                    details = (e.infector, e.infected, e.case.case_num, e.description)
                    context['data'][event].append(details)

            if not context['data']:
                context['empty'] = True
        
    return render(request, template_name, context)