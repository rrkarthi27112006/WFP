from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import StudentRegisterForm, TeacherRegisterForm


def register_choice(request):
    return render(request, 'accounts/register_choice.html')


def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to EduTrack! Your student account has been created.')
            return redirect('dashboard:redirect')
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts/register_student.html', {'form': form})


def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to EduTrack! Your teacher account has been created.')
            return redirect('dashboard:redirect')
    else:
        form = TeacherRegisterForm()
    return render(request, 'accounts/register_teacher.html', {'form': form})


class EduTrackLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def edutrack_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')
