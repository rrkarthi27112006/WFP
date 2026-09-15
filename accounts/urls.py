from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.EduTrackLoginView.as_view(), name='login'),
    path('logout/', views.edutrack_logout, name='logout'),
]

