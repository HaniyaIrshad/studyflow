from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),

    # Subjects
    path('subjects/', views.subjects, name='subjects'),
    path('subjects/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),

    # Tasks
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    # Notes
    path('notes/', views.notes, name='notes'),

    # Today view
    path('tasks/today/', views.today_tasks, name='today_tasks'),
]