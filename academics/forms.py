from django import forms
from .models import ClassRoom, Subject, School
from accounts.models import StudentProfile


class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'school', 'class_teacher']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'classes', 'teacher']
        widgets = {'classes': forms.CheckboxSelectMultiple}


class StudentAssignForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['student_class', 'roll_number', 'school', 'parent']
