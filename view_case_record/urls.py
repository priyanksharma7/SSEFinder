from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:location_id>/', views.detail, name='view_case_record'),
]