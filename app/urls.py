from django.urls import path
from .views import *
from .models import Case

urlpatterns = [
    path('', Home, name='home'),
    path('case/', Showcase, name='addcase'),
    path('event/', Showevent, name='showevent'),
    path('addevent/', Addevent, name='addevent'),
    path('list', SSE, name='sse-list'),
    path('search', SearchCase, name='searchcase'),
]