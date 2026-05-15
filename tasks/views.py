from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Subject, Task
from .forms import SubjectForm, TaskForm


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def subjects(request):

    if request.method == 'POST':

        form = SubjectForm(request.POST)

        if form.is_valid():

            subject = form.save(commit=False)

            subject.user = request.user

            subject.save()

            return redirect('subjects')

    else:

        form = SubjectForm()

    subjects = Subject.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'subjects.html', {
        'form': form,
        'subjects': subjects
    })


@login_required
def tasks(request):

    if request.method == 'POST':

        form = TaskForm(request.POST)

        # show only current user's subjects
        form.fields['subject'].queryset = Subject.objects.filter(
            user=request.user
        )

        if form.is_valid():

            task = form.save(commit=False)

            # security check
            if task.subject.user == request.user:

                task.save()

                return redirect('tasks')

    else:

        form = TaskForm()

        form.fields['subject'].queryset = Subject.objects.filter(
            user=request.user
        )

    pending_tasks = Task.objects.filter(
        subject__user=request.user,
        completed=False
    ).order_by('-created_at')

    completed_tasks = Task.objects.filter(
        subject__user=request.user,
        completed=True
    ).order_by('-created_at')

    return render(request, 'tasks.html', {
    'form': form,
    'pending_tasks': pending_tasks,
    'completed_tasks': completed_tasks,
    'today': timezone.now().date()
})


@login_required
def toggle_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        subject__user=request.user
    )

    task.completed = not task.completed

    task.save()

    return redirect('tasks')


@login_required
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        subject__user=request.user
    )

    task.delete()

    return redirect('tasks')

@login_required
def edit_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        subject__user=request.user
    )

    if request.method == 'POST':

        form = TaskForm(request.POST, instance=task)

        if form.is_valid():

            updated_task = form.save(commit=False)

            if updated_task.subject.user == request.user:

                updated_task.save()

                return redirect('tasks')

    else:

        form = TaskForm(instance=task)

        form.fields['subject'].queryset = Subject.objects.filter(
            user=request.user
        )

    return render(request, 'edit_task.html', {
        'form': form
    })



@login_required
def dashboard(request):

    user_tasks = Task.objects.filter(
        subject__user=request.user
    )

    total_tasks = user_tasks.count()

    completed_tasks = user_tasks.filter(
        completed=True
    ).count()

    pending_tasks = user_tasks.filter(
        completed=False
    ).count()

    overdue_tasks = user_tasks.filter(
        completed=False,
        due_date__lt=timezone.now().date()
    ).count()

    recent_tasks = user_tasks.order_by(
        '-created_at'
    )[:5]

    upcoming_tasks = user_tasks.filter(
        completed=False,
        due_date__gte=timezone.now().date()
    ).order_by('due_date')[:5]

    return render(request, 'dashboard.html', {

        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,

        'recent_tasks': recent_tasks,
        'upcoming_tasks': upcoming_tasks,
    })
