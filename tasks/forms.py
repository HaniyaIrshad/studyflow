from django import forms
from .models import Subject, Task, Note


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter subject name',
                'class': 'form-input'
            })
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['subject', 'title', 'due_date', 'priority']

        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-select'
            }),

            'title': forms.TextInput(attrs={
                'placeholder': 'Enter task',
                'class': 'form-input'
            }),

            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),

            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Restrict subjects to logged-in user (IMPORTANT SECURITY + CLEAN DESIGN)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)

        # Optional UX improvement: ordering
        self.fields['subject'].empty_label = "Select Subject"


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['subject', 'title', 'content']

        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-select'
            }),

            'title': forms.TextInput(attrs={
                'placeholder': 'Enter note title',
                'class': 'form-input'
            }),

            'content': forms.Textarea(attrs={
                'placeholder': 'Write your note here...',
                'class': 'form-textarea'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Restrict notes to user's subjects
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)

        self.fields['subject'].empty_label = "Select Subject"