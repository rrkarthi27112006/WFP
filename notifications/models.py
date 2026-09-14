from django.db import models
from django.contrib.auth.models import User

NOTIFICATION_TYPES = [
    ('task_assigned', 'New Task Assigned'),
    ('deadline', 'Upcoming Deadline'),
    ('feedback', 'Teacher Feedback'),
    ('reviewed', 'Submission Reviewed'),
    ('announcement', 'New Announcement'),
    ('new_submission', 'New Student Submission'),
    ('missing_work', 'Missing Student Work'),
]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user}: {self.message}'


class Announcement(models.Model):
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    message = models.TextField()
    target_class = models.ForeignKey(
        'academics.ClassRoom', on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements'
    )
    target_all_students = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
