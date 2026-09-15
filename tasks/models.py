# pyrefly: ignore [missing-import]
from django.db import models
# pyrefly: ignore [missing-import]
from django.utils import timezone


TASK_TYPE_CHOICES = [
    ('homework', 'Homework'),
    ('project', 'Project'),
    ('worksheet', 'Worksheet'),
    ('reading', 'Reading'),
    ('class_activity', 'Class Activity'),
    ('quiz', 'Quiz'),
    ('revision', 'Revision Task'),
]

DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

IMPORTANCE_CHOICES = [
    ('normal', 'Normal'),
    ('important', 'Important'),
    ('critical', 'Critical'),
]


def task_attachment_path(instance, filename):
    return f'task_attachments/{instance.pk or "new"}/{filename}'


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.CASCADE, related_name='tasks')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='tasks')

    class_assigned = models.ForeignKey(
        'academics.ClassRoom', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks'
    )
    student = models.ForeignKey(
        'accounts.StudentProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='individual_tasks',
        help_text='Set this to assign the task to a single student instead of a whole class.'
    )

    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='homework')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    importance = models.CharField(max_length=10, choices=IMPORTANCE_CHOICES, default='normal')

    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1, default=1.0,
                                           help_text='Estimated completion time, in hours.')
    max_marks = models.PositiveIntegerField(default=10)
    due_date = models.DateTimeField()

    attachment = models.FileField(upload_to=task_attachment_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title

    def target_students(self):
        """Return a queryset of StudentProfiles this task applies to."""
        from accounts.models import StudentProfile
        if self.student_id:
            return StudentProfile.objects.filter(pk=self.student_id)
        if self.class_assigned_id:
            return self.class_assigned.students.all()
        return StudentProfile.objects.none()

    def is_overdue(self):
        return timezone.now() > self.due_date

    def hours_remaining(self):
        delta = self.due_date - timezone.now()
        return round(delta.total_seconds() / 3600, 1)

    # ---- Smart Priority System ----
    def smart_priority_score(self):
        """
        Higher score = more urgent/important.
        Weighs: time remaining, difficulty, estimated effort, marks weight.
        """
        hours_left = max(self.hours_remaining(), 0.1)
        urgency = 100 / hours_left  # closer due date -> higher urgency

        difficulty_weight = {'easy': 1, 'medium': 2, 'hard': 3}.get(self.difficulty, 2)
        effort_weight = float(self.estimated_hours)
        marks_weight = self.max_marks / 10.0
        importance_bonus = {'normal': 0, 'important': 5, 'critical': 12}.get(self.importance, 0)

        score = (urgency * 1.5) + (difficulty_weight * 4) + (effort_weight * 2) + marks_weight + importance_bonus
        return round(score, 2)

    def smart_priority_label(self):
        score = self.smart_priority_score()
        if self.is_overdue():
            return 'HIGH'
        if score >= 30:
            return 'HIGH'
        elif score >= 15:
            return 'MEDIUM'
        return 'LOW'

    def smart_priority_reason(self):
        parts = []
        if self.is_overdue():
            parts.append('it is overdue')
        else:
            hrs = self.hours_remaining()
            if hrs <= 24:
                parts.append('it is due within 24 hours')
            elif hrs <= 72:
                parts.append(f'it is due in about {round(hrs / 24)} day(s)')
            else:
                parts.append(f'it is due in about {round(hrs / 24)} days')

        if self.difficulty == 'hard':
            parts.append('has high difficulty')
        elif self.difficulty == 'medium':
            parts.append('has moderate difficulty')

        parts.append(f'requires approximately {self.estimated_hours} hour(s)')

        if self.importance == 'critical':
            parts.append('is marked critical by the teacher')

        label = self.smart_priority_label().title()
        reason = ', '.join(parts)
        # Make the last comma an "and"
        if ', ' in reason:
            head, tail = reason.rsplit(', ', 1)
            reason = f'{head}, and {tail}'
        return f'{label} priority because {reason}.'
