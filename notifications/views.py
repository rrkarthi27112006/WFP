from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.decorators import teacher_required, student_required, parent_required
from .models import Notification, Announcement
from .forms import AnnouncementForm
from .utils import notify_announcement


@teacher_required
def announcement_list(request):
    teacher = request.user.teacher_profile
    announcements = Announcement.objects.filter(teacher=teacher)
    return render(request, 'notifications/teacher_announcement_list.html', {'announcements': announcements})


@teacher_required
def announcement_create(request):
    teacher = request.user.teacher_profile
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.teacher = teacher
            ann.save()
            notify_announcement(ann)
            messages.success(request, 'Announcement posted.')
            return redirect('notifications:announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'notifications/announcement_form.html', {'form': form})


def _announcements_for_user(user):
    if hasattr(user, 'student_profile'):
        student = user.student_profile
        from django.db.models import Q
        return Announcement.objects.filter(
            Q(target_all_students=True) | Q(target_class=student.student_class)
        ).distinct()
    if hasattr(user, 'parent_profile'):
        from django.db.models import Q
        classes = [c.student_class_id for c in user.parent_profile.children.all() if c.student_class_id]
        return Announcement.objects.filter(Q(target_all_students=True) | Q(target_class_id__in=classes)).distinct()
    return Announcement.objects.none()


def my_announcements(request):
    announcements = _announcements_for_user(request.user) if request.user.is_authenticated else Announcement.objects.none()
    return render(request, 'notifications/my_announcements.html', {'announcements': announcements})


def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})
