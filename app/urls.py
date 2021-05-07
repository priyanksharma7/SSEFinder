from django.urls import path
from .views import *
from .models import Case

urlpatterns = [
    path('', Base, name='base'),
    path('case/', Showcase, name='addcase'),
    path('event/', Showevent, name='showevent'),
    path('addevent/', Addevent, name='addevent'),
    path('list', SSE, name='sse-list'),
    path('view_case_record', view_case_record_index, name='index'),
    path('<int:case_id>/', view_case_record_details, name='view_case_record'),
]