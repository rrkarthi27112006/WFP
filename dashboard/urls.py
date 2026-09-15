from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('redirect/', views.role_redirect, name='redirect'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('progress/', views.student_progress, name='student_progress'),
    path('workload/', views.student_workload, name='student_workload'),
    path('deadlines/', views.deadlines_calendar, name='deadlines_calendar'),
    path('reports/', views.teacher_reports, name='teacher_reports'),
]

