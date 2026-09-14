from django.contrib import admin
from .models import StudentProfile, TeacherProfile, ParentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_class', 'roll_number', 'school', 'parent')
    list_filter = ('student_class', 'school')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'roll_number')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'qualification', 'phone')
    list_filter = ('school',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
