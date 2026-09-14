from django.db import models
from django.utils import timezone

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('submitted', 'Submitted'),
    ('reviewed', 'Reviewed'),
    ('overdue', 'Overdue'),
]


def submission_file_path(instance, filename):
    return f'submissions/{instance.task_id}/{instance.student_id}/{filename}'


def submission_image_path(instance, filename):
    return f'submissions/{instance.task_id}/{instance.student_id}/images/{filename}'


class Submission(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='submissions')

    text_answer = models.TextField(blank=True)
    file = models.FileField(upload_to=submission_file_path, blank=True, null=True)
    image = models.ImageField(upload_to=submission_image_path, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    marks_obtained = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    is_resubmission_allowed = models.BooleanField(default=False)
    submission_count = models.PositiveIntegerField(default=0)

    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('task', 'student')
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.student} -> {self.task}'

    def effective_status(self):
        """Status accounting for overdue tasks that were never submitted."""
        if self.status in ('pending', 'in_progress') and self.task.is_overdue():
            return 'overdue'
        return self.status

    def mark_submitted(self):
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.submission_count += 1
