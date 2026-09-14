from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from academics.models import ClassRoom, School
from .models import StudentProfile, TeacherProfile


class StudentRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=False)
    student_class = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), required=False, label='Class')
    roll_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        StudentProfile.objects.create(
            user=user,
            school=self.cleaned_data.get('school'),
            student_class=self.cleaned_data.get('student_class'),
            roll_number=self.cleaned_data.get('roll_number', ''),
        )
        return user


class TeacherRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=False)
    qualification = forms.CharField(max_length=150, required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        TeacherProfile.objects.create(
            user=user,
            school=self.cleaned_data.get('school'),
            qualification=self.cleaned_data.get('qualification', ''),
            phone=self.cleaned_data.get('phone', ''),
        )
        return user
