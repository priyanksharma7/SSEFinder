from django.shortcuts import render
from .forms import Caseform, Eventform
from django.http import HttpResponse, HttpResponseRedirect
from .models import Case, Event
from datetime import datetime, timedelta, date

from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Max, Min
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def Base(request):
    template_name = 'base.html'

    return render(request, template_name)


def Showcase(request):
    form = Caseform()

    return render(request, 'addcase.html', {'form': form})


def Showevent(request):
    #This function first stores the Case data and
    #then renders the add event form
    form1 = Eventform()
    if request.method == 'POST':
        form = Caseform(request.POST)
        if form.is_valid():
            new_case = form.save()
            form1 = Eventform(initial={'case': new_case})
            # form1.fields['case'].widget.attrs['readonly'] = True
            # form1.fields['case'].disabled = True
        else:
            form1 = Eventform()

    return render(request, 'addevent.html', {'form': form1})


def Addevent(request):
    #This function first stores the previously entered even
    #and then renders the add event form again.

    form = Eventform(request.POST)
    if form.is_valid():
        min_date = Case.objects.get(
            id=form.data['case']).date_of_onset - timedelta(14)
        max_date = Case.objects.get(id=form.data['case']).date_of_confirmation
        e_date = datetime.strptime(form.data['date'], '%Y-%m-%d').date()
        if e_date < min_date:
            return render(
                request, 'dateerror.html', {
                    'errormessage':
                    "The date of Event is before the 14th day, Do not add this event or change date"
                })

        if e_date > max_date:
            return render(
                request, 'dateerror.html', {
                    'errormessage':
                    "The date of Event is after the date of confirmation, Do   not add this event or change date"
                })

        form.save()
    form1 = Eventform()
    return render(request, 'addevent.html', {'form': form1})


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
                    event = (e.venue_name, e.venue_location, e.address,
                             e.x_coordinate, e.y_coordinate, e.date)
                    if event not in context['data']:
                        context['data'][event] = []
                    details = (e.infector, e.infected, e.case.case_num,
                               e.description)
                    context['data'][event].append(details)

            if not context['data']:
                context['empty'] = True

    return render(request, template_name, context)


def view_case_record_index(request):
    """ Index page (details), showing lastest case
        Author: Aero
    """
    try:
        # get lastest case id
        default_case_id = Case.objects.all().aggregate(
            Max('case_num'))['case_num__max']
        return view_case_record_details(request, default_case_id)
    except ObjectDoesNotExist:
        return view_case_record_details(request, 0)


def view_case_record_details(request, case_id):
    """ Details page, allowing users to search a particular user by case id
        Author: Aero 
    """
    if request.method == 'POST':
        form = CaseNumberForm(request.POST)
        if form.is_valid():
            try:
                case_number = form.cleaned_data['case_number']
                return redirect('view_case_record', case_id=case_number)
            except:
                redirect('index')
        else:
            redirect('index')

    try:
        case = Case.objects.get(case_num=case_id)
        context = {
            'case_num': case.case_num,
            'patient_name': case.patient_name,
            'id_num': case.id_num,
            'date_of_birth': case.date_of_birth,
            'date_of_onset': case.date_of_onset,
            'date_of_confirmation': case.date_of_confirmation,
            'search_form': CaseNumberForm()
        }
    except ObjectDoesNotExist:
        context = {
            'data': {
                'error':
                'Case does not exist in database, please add a new Case.'
            }
        }
    return render(request, 'view_case_record/index.html', context)


class CaseNumberForm(forms.Form):
    """ Author: Aero
    """
    cases = Case.objects.all()
    max_case = cases.aggregate(Max('case_num'))['case_num__max']
    min_case = cases.aggregate(Min('case_num'))['case_num__min']

    case_number = forms.IntegerField(max_value=max_case, min_value=min_case)