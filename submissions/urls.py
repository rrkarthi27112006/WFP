from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    path('submit/<int:pk>/', views.submit_task, name='submit_task'),
    path('review/<int:pk>/', views.review_submission, name='review_submission'),
]
