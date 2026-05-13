from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Subject,Task
from .forms import SubjectForm,TaskForm

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

    subjects = Subject.objects.filter(user=request.user)

    return render(request, 'subjects.html', {
        'form': form,
        'subjects': subjects
    })

@login_required
def tasks(request):

    if request.method == 'POST':

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            if task.subject.user == request.user:

                task.save()

                return redirect('tasks')

    else:

        form = TaskForm()

        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

    tasks = Task.objects.filter(subject__user=request.user)

    return render(request, 'tasks.html', {
        'form': form,
        'tasks': tasks
    })