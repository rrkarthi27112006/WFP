from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'subject', 'class_assigned', 'student', 'task_type', 'difficulty', 'due_date')
    list_filter = ('task_type', 'difficulty', 'importance', 'subject')
    search_fields = ('title', 'description')
