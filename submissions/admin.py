from django.contrib import admin
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'status', 'marks_obtained', 'submitted_at', 'reviewed_at')
    list_filter = ('status',)
    search_fields = ('task__title', 'student__user__username')
