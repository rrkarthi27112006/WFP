from django.contrib import admin
from .models import School, ClassRoom, Subject


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name',)


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'class_teacher', 'student_count')
    list_filter = ('school', 'class_teacher')
    search_fields = ('name',)
    filter_horizontal = ('students',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'get_teachers_display')
    list_filter = ('classes', 'teachers')
    search_fields = ('name', 'code')
    filter_horizontal = ('teachers', 'classes')

    def get_teachers_display(self, obj):
        return ", ".join([str(t) for t in obj.teachers.all()]) or "None"
    get_teachers_display.short_description = 'Teachers'

