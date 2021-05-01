from django.urls import path
from .views import *
from .models import Case

urlpatterns = [
    path('', Base, name='base'),
    path('case/', Showcase, name='addcase'),
    path('event/', Showevent, name='showevent'),
    path('addevent/', Addevent, name='addevent'),
    path('list', SSE, name='sse-list'),
]