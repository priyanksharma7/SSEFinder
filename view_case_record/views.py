from app.models import Case
from django.shortcuts import render

from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Max, Min
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def index(request):
    """Index page (details), showing lastest case
    """
    try:
        # get lastest case id
        default_case_id = Case.objects.all.aggregate(Max('case_num')).pk
        return details(request, default_case_id)
    except ObjectDoesNotExist:
        return details(request, 0)


def details(request, case_id):
    """Details page, allowing users to search a particular user by case id
    """
    if request.method == 'POST':
        form = CaseNumberForm(request.POST)
        if form.is_valid():
            try:
                case_number = form.cleaned_data['case_number']
                return redirect(case_number)
            except:
                redirect('index')

    try:
        case = Case.objects.get(pk=case_id)
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
    cases = Case.objects.all()
    max_case = cases.aggregate(Max('case_num'))
    min_case = cases.aggregate(Min('case_num'))

    case_number = forms.IntegerField(max_value=max_case, min_value=min_case)
