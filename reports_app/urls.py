# reports_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.weekly_task_report, name='weekly_task_report'),
    path('habits/', views.weekly_habit_report, name='weekly_habit_report'),  # habit report
]
