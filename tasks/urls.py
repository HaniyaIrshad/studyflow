from django.urls import path
from .views import home, dashboard, subjects, tasks, toggle_task
urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('subjects/', subjects, name='subjects'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/toggle/<int:task_id>/', toggle_task, name='toggle_task'),
]