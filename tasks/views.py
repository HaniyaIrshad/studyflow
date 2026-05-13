from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Subject
from .forms import SubjectForm

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