from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from accounts.decorators import student_required, teacher_required
from .models import Submission
from .forms import SubmissionForm, ReviewForm
from notifications.utils import notify_new_submission, notify_reviewed


@student_required
def submit_task(request, pk):
    student = request.user.student_profile
    submission = get_object_or_404(Submission, pk=pk, student=student)
    task = submission.task

    if task.is_overdue() and submission.status == 'pending':
        messages.warning(request, 'This task is overdue. You can still submit, but it will be flagged.')

    if submission.status in ('submitted', 'reviewed') and not submission.is_resubmission_allowed:
        messages.error(request, 'This task has already been submitted and resubmission is not allowed.')
        return redirect('tasks:student_task_detail', pk=task.id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.mark_submitted()
            if sub.is_resubmission_allowed:
                sub.is_resubmission_allowed = False
            sub.save()
            notify_new_submission(sub)
            messages.success(request, 'Your work has been submitted successfully.')
            return redirect('tasks:student_task_detail', pk=task.id)
    else:
        form = SubmissionForm(instance=submission)

    return render(request, 'submissions/submit_task.html', {'form': form, 'task': task, 'submission': submission})


@teacher_required
def review_submission(request, pk):
    teacher = request.user.teacher_profile
    submission = get_object_or_404(Submission, pk=pk, task__teacher=teacher)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=submission)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.status = 'reviewed'
            sub.reviewed_at = timezone.now()
            sub.save()
            notify_reviewed(sub)
            messages.success(request, 'Review submitted successfully.')
            return redirect('tasks:teacher_task_detail', pk=submission.task.id)
    else:
        form = ReviewForm(instance=submission)

    return render(request, 'submissions/review_submission.html', {'form': form, 'submission': submission})
