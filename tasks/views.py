from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Subject, Task, Note
from .forms import SubjectForm, TaskForm, NoteForm


def home(request):
    return render(request, 'home.html')


@login_required
def subjects(request):

    if request.method == 'POST':

        form = SubjectForm(request.POST)

        if form.is_valid():

            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()

            messages.success(request, "Subject added successfully!")

            return redirect('subjects')

        else:
            messages.error(request, "Please correct the errors in subject form.")

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
def edit_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    if request.method == 'POST':

        subject.name = request.POST.get('name')
        subject.save()

        messages.success(request, "Subject updated successfully!")

        return redirect('subjects')

    return render(request, 'edit_subject.html', {
        'subject': subject
    })


@login_required
def delete_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    subject.delete()

    messages.success(request, "Subject deleted successfully!")

    return redirect('subjects')


@login_required
def tasks(request):

    if request.method == 'POST':

        form = TaskForm(request.POST)

        form.fields['subject'].queryset = Subject.objects.filter(
            user=request.user
        )

        if form.is_valid():

            task = form.save(commit=False)

            if task.subject.user == request.user:

                task.save()

                messages.success(request, "Task added successfully!")

                return redirect('tasks')

        else:
            messages.error(request, "Please correct the task form.")

    else:

        form = TaskForm()

        form.fields['subject'].queryset = Subject.objects.filter(
            user=request.user
        )

    tasks = Task.objects.filter(
        subject__user=request.user
    )

    search = request.GET.get('search')

    if search:
        tasks = tasks.filter(title__icontains=search)

    priority = request.GET.get('priority')
    status = request.GET.get('status')
    subject = request.GET.get('subject')

    if priority:
        tasks = tasks.filter(priority=priority)

    if status == 'completed':
        tasks = tasks.filter(completed=True)

    elif status == 'pending':
        tasks = tasks.filter(completed=False)

    if subject:
        tasks = tasks.filter(subject_id=subject)

    tasks = tasks.order_by('completed', '-created_at')

    pending_tasks = tasks.filter(completed=False)
    completed_tasks = tasks.filter(completed=True)

    return render(request, 'tasks.html', {
        'form': form,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'today': timezone.now().date(),
        'subjects': Subject.objects.filter(user=request.user),
        'selected_priority': priority,
        'selected_status': status,
        'selected_subject': subject,
        'search_query': search,
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

    messages.success(request, "Task status updated!")

    return redirect('tasks')


@login_required
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        subject__user=request.user
    )

    task.delete()

    messages.success(request, "Task deleted successfully!")

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

        form.fields['subject'].queryset = Subject.objects.filter(
            user=request.user
        )

        if form.is_valid():

            updated_task = form.save(commit=False)

            if updated_task.subject.user == request.user:

                updated_task.save()

                messages.success(request, "Task updated successfully!")

                return redirect('tasks')

        else:
            messages.error(request, "Please correct the task form.")

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
    completed_tasks = user_tasks.filter(completed=True).count()
    pending_tasks = user_tasks.filter(completed=False).count()

    overdue_tasks = user_tasks.filter(
        completed=False,
        due_date__lt=timezone.now().date()
    ).count()

    recent_tasks = user_tasks.order_by('-created_at')[:5]

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


@login_required
def notes(request):

    notes = Note.objects.filter(
        subject__user=request.user
    )

    form = NoteForm()

    if request.method == 'POST':

        form = NoteForm(request.POST)

        if form.is_valid():

            note = form.save(commit=False)

            if note.subject.user == request.user:

                note.save()

                messages.success(request, "Note added successfully!")

                return redirect('notes')

        else:
            messages.error(request, "Please correct the note form.")

    return render(request, 'notes.html', {
        'notes': notes,
        'form': form
    })


@login_required
def today_tasks(request):

    today = timezone.now().date()

    tasks = Task.objects.filter(
        subject__user=request.user,
        due_date=today
    )

    return render(request, 'today_tasks.html', {
        'tasks': tasks
    })