from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.decorators import teacher_required
from accounts.models import StudentProfile
from .models import ClassRoom, Subject
from .forms import ClassRoomForm, SubjectForm, StudentAssignForm


@teacher_required
def class_list(request):
    teacher = request.user.teacher_profile
    classes = ClassRoom.objects.filter(class_teacher=teacher) or ClassRoom.objects.all()
    return render(request, 'academics/class_list.html', {'classes': classes})


@teacher_required
def class_create(request):
    if request.method == 'POST':
        form = ClassRoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class created successfully.')
            return redirect('academics:class_list')
    else:
        form = ClassRoomForm(initial={'class_teacher': request.user.teacher_profile})
    return render(request, 'academics/class_form.html', {'form': form, 'title': 'Create Class'})


@teacher_required
def class_edit(request, pk):
    classroom = get_object_or_404(ClassRoom, pk=pk)
    if request.method == 'POST':
        form = ClassRoomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully.')
            return redirect('academics:class_list')
    else:
        form = ClassRoomForm(instance=classroom)
    return render(request, 'academics/class_form.html', {'form': form, 'title': 'Edit Class'})


@teacher_required
def class_delete(request, pk):
    classroom = get_object_or_404(ClassRoom, pk=pk)
    if request.method == 'POST':
        classroom.delete()
        messages.success(request, 'Class deleted.')
        return redirect('academics:class_list')
    return render(request, 'academics/confirm_delete.html', {'object': classroom, 'type': 'class'})


@teacher_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'academics/subject_list.html', {'subjects': subjects})


@teacher_required
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully.')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'academics/subject_form.html', {'form': form, 'title': 'Create Subject'})


@teacher_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'academics/subject_form.html', {'form': form, 'title': 'Edit Subject'})


@teacher_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted.')
        return redirect('academics:subject_list')
    return render(request, 'academics/confirm_delete.html', {'object': subject, 'type': 'subject'})


@teacher_required
def student_list(request):
    class_filter = request.GET.get('class', '')
    students = StudentProfile.objects.select_related('user', 'student_class').all()
    if class_filter:
        students = students.filter(student_class_id=class_filter)
    classes = ClassRoom.objects.all()
    return render(request, 'academics/student_list.html', {
        'students': students, 'classes': classes, 'class_filter': class_filter,
    })


@teacher_required
def student_edit(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    if request.method == 'POST':
        form = StudentAssignForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student details updated.')
            return redirect('academics:student_list')
    else:
        form = StudentAssignForm(instance=student)
    return render(request, 'academics/student_form.html', {'form': form, 'student': student})
