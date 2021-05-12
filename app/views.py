from django.shortcuts import render, redirect
from .models import Case, Event
from .forms import CaseForm, EventForm
import requests
import json
from urllib.parse import urljoin
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def Home(request):
    template_name = 'home.html'
    return render(request, template_name)

@login_required
def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            if case.date_of_onset > case.date_of_confirmation:
                form.add_error('date_of_onset', "Date of Onset should not be after Date of Confirmation")
            else:
                form.save()
                request.session['case'] = form.cleaned_data['case_num']
                messages.success(request, 'Case Record was saved successfully!')
                return redirect('event-create')
    else:
        form = CaseForm()
    return render(request, 'case_form.html', {'form': form})

@login_required
def event_create(request):
    casedata = Case.objects.get(case_num = request.session['case'])
    if request.method == 'POST':
        redirect_url = 'home'
        if 'save' in request.POST:
            redirect_url = 'event-create'
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.case = casedata
            event_function(event)
            
            if event.date >= event.case.date_of_onset - timedelta(14) and event.date <= event.case.date_of_confirmation:
                event.save()
                messages.success(request, 'Social Event was saved successfully!')
                return redirect(redirect_url)
            else:
                form.add_error('date', "Date of event should be 14 days before the onset of symptoms up to and including the day of confirmation of infection")
    
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form, 'case': casedata})

# Helper function
def event_function(event):
    # Location API
    url = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch"

    temp = str(event.venue_location)
    query = "?q=" + temp.replace(" ","%20")
    final_url = urljoin(url, query)
    r = requests.get(url = final_url)
    if r.status_code == 200:
        data = r.json()
        data = data[0]
        event.address = data['addressEN']
        event.x_coordinate =  float(data['x'])
        event.y_coordinate =  float(data['y'])
    else:
        event.x_coordinate =  0.0
        event.y_coordinate =  0.0
        event.address = "-"

    # Check for infector
    if event.date >= event.case.date_of_onset - timedelta(days=3) and event.date <= event.case.date_of_confirmation:
        event.infector = True
    # Check for infected
    if event.case.date_of_onset >= event.date + timedelta(days=2) and event.case.date_of_onset <= event.date + timedelta(days=14):
        event.infected = True

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

        startdate = datetime.strptime(start, '%Y-%m-%d').date()
        enddate = datetime.strptime(end, '%Y-%m-%d').date()

        if startdate > enddate:
            context['error'] = "Error: Start Date should be before End Date"

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