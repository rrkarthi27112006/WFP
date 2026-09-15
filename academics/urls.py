from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('classes/', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/<int:pk>/edit/', views.class_edit, name='class_edit'),
    path('classes/<int:pk>/delete/', views.class_delete, name='class_delete'),

    path('subjects/', views.subject_list, name='subject_list'),
    path('students/', views.student_list, name='student_list'),
]

