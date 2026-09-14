from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.EduTrackLoginView.as_view(), name='login'),
    path('logout/', views.edutrack_logout, name='logout'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
]
