from django.shortcuts import render

# Create your views here.

def Base(request):
    template_name = 'base.html'

    return render(request, template_name)