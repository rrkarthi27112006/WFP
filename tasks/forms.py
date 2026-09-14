from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'subject', 'class_assigned', 'student',
            'task_type', 'difficulty', 'importance', 'estimated_hours',
            'max_marks', 'due_date', 'attachment',
        ]
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher is not None:
            from academics.models import Subject, ClassRoom
            self.fields['subject'].queryset = Subject.objects.all()
            self.fields['class_assigned'].queryset = ClassRoom.objects.all()
        self.fields['class_assigned'].required = False
        self.fields['student'].required = False

    def clean(self):
        cleaned_data = super().clean()
        class_assigned = cleaned_data.get('class_assigned')
        student = cleaned_data.get('student')
        if not class_assigned and not student:
            raise forms.ValidationError(
                'Assign this task to either a class or an individual student.'
            )
        return cleaned_data
