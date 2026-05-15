from django.urls import path

from .views import (
    home,
    dashboard,
    subjects,
    tasks,
    toggle_task,
    delete_task,
    edit_task,
    edit_subject,
    delete_subject,
    notes,
    today_tasks
)

urlpatterns = [

    path('', home, name='home'),

    path('dashboard/', dashboard, name='dashboard'),

    path('subjects/', subjects, name='subjects'),

    path(
        'subject/edit/<int:subject_id>/',
        edit_subject,
        name='edit_subject'
    ),

    path(
        'subject/delete/<int:subject_id>/',
        delete_subject,
        name='delete_subject'
    ),

    path('tasks/', tasks, name='tasks'),

    path(
        'tasks/toggle/<int:task_id>/',
        toggle_task,
        name='toggle_task'
    ),

    path(
        'tasks/delete/<int:task_id>/',
        delete_task,
        name='delete_task'
    ),

    path(
        'tasks/edit/<int:task_id>/',
        edit_task,
        name='edit_task'
    ),
    path('notes/', notes, name='notes'),
    path(
    'today/',today_tasks,
    name='today_tasks'
),

]