from django.urls import path
from .views import home, dashboard, subjects,tasks

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('subjects/', subjects, name='subjects'),
    path('tasks/', tasks, name='tasks'),
]