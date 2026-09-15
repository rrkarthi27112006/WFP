from django import forms
from .models import ClassRoom, Subject
from accounts.models import StudentProfile


class ClassRoomForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=StudentProfile.objects.select_related('user').all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Select the students to include in this class.'
    )

    class Meta:
        model = ClassRoom
        fields = ['name', 'students']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'classes', 'teachers']
        widgets = {
            'classes': forms.CheckboxSelectMultiple,
            'teachers': forms.CheckboxSelectMultiple,
        }

