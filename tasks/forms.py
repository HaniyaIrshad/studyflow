from django import forms
from .models import Subject, Task, Note


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ['name']


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['subject', 'title', 'due_date', 'priority']

        widgets = {

            'due_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter task'
                }
            ),
        }


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['subject', 'title', 'content']