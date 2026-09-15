from django import forms
from .models import Task
from accounts.models import StudentProfile


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
            teacher_subjects = Subject.objects.filter(teachers=teacher)
            self.fields['subject'].queryset = teacher_subjects if teacher_subjects.exists() else Subject.objects.all()
            
            teacher_classes = ClassRoom.objects.filter(class_teacher=teacher)
            self.fields['class_assigned'].queryset = teacher_classes if teacher_classes.exists() else ClassRoom.objects.all()
        
        self.fields['student'].queryset = StudentProfile.objects.select_related('user').all()
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

