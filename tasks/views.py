from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Subject, Task, Note
from .forms import SubjectForm, TaskForm, NoteForm


# -------------------------
# HELPERS (DRY IMPROVEMENT)
# -------------------------

def get_user_subjects(user):
    return Subject.objects.filter(user=user)


def get_user_tasks(user):
    return Task.objects.filter(subject__user=user)


# -------------------------
# HOME
# -------------------------

def home(request):
    return render(request, 'home.html')


# -------------------------
# SUBJECTS
# -------------------------

@login_required
def subjects(request):

    form = SubjectForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        subject = form.save(commit=False)
        subject.user = request.user
        subject.save()

        messages.success(request, "Subject added successfully!")
        return redirect('subjects')

    subjects_qs = get_user_subjects(request.user).order_by('-created_at')

    return render(request, 'subjects.html', {
        'form': form,
        'subjects': subjects_qs
    })


@login_required
def edit_subject(request, subject_id):

    subject = get_object_or_404(Subject, id=subject_id, user=request.user)

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

    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.delete()

    messages.success(request, "Subject deleted successfully!")
    return redirect('subjects')


# -------------------------
# TASKS
# -------------------------

@login_required
def tasks(request):

    form = TaskForm(request.POST or None)
    form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.save()

        messages.success(request, "Task added successfully!")
        return redirect('tasks')

    tasks_qs = Task.objects.filter(subject__user=request.user)

    # Filters
    search = request.GET.get('search', '').strip()
    priority = request.GET.get('priority')
    status = request.GET.get('status')
    subject = request.GET.get('subject')

    if search:
        tasks_qs = tasks_qs.filter(title__icontains=search)

    if priority:
        tasks_qs = tasks_qs.filter(priority=priority)

    if status == 'completed':
        tasks_qs = tasks_qs.filter(completed=True)
    elif status == 'pending':
        tasks_qs = tasks_qs.filter(completed=False)

    if subject and subject.isdigit():
        tasks_qs = tasks_qs.filter(subject_id=int(subject))

    tasks_qs = tasks_qs.order_by('completed', '-created_at')

    return render(request, 'tasks.html', {
        'form': form,
        'pending_tasks': tasks_qs.filter(completed=False),
        'completed_tasks': tasks_qs.filter(completed=True),
        'today': timezone.now().date(),
        'subjects': Subject.objects.filter(user=request.user),
        'selected_priority': priority,
        'selected_status': status,
        'selected_subject': subject,
        'search_query': search,
    })

@login_required
def toggle_task(request, task_id):

    task = get_object_or_404(Task, id=task_id, subject__user=request.user)
    task.completed = not task.completed
    task.save()

    messages.success(request, "Task status updated!")
    return redirect('tasks')


@login_required
def delete_task(request, task_id):

    task = get_object_or_404(Task, id=task_id, subject__user=request.user)
    task.delete()

    messages.success(request, "Task deleted successfully!")
    return redirect('tasks')


@login_required
def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id, subject__user=request.user)

    form = TaskForm(request.POST or None, instance=task, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Task updated successfully!")
        return redirect('tasks')

    return render(request, 'edit_task.html', {
        'form': form
    })


# -------------------------
# DASHBOARD
# -------------------------

@login_required
def dashboard(request):

    user_tasks = get_user_tasks(request.user)

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


# -------------------------
# NOTES
# -------------------------

@login_required
def notes(request):

    form = NoteForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)

        if note.subject.user == request.user:
            note.save()
            messages.success(request, "Note added successfully!")
            return redirect('notes')

    notes_qs = Note.objects.filter(subject__user=request.user)

    return render(request, 'notes.html', {
        'notes': notes_qs,
        'form': form
    })


# -------------------------
# TODAY TASKS
# -------------------------

@login_required
def today_tasks(request):

    today = timezone.now().date()

    tasks_qs = Task.objects.filter(
        subject__user=request.user,
        due_date=today
    )

    return render(request, 'today_tasks.html', {
        'tasks': tasks_qs
    })