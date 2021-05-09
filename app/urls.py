from django.urls import path
from .views import *
from .models import Case

urlpatterns = [
    path('', Home, name='home'),
    path('createcase/', case_create, name='case-create'),
    path('createevent/', event_create, name='event-create'),
    path('search', SearchCase, name='search-case'),
    path('list', SSE, name='sse-list'),
]