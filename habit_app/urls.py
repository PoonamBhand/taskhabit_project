# habit_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # List all habits
    path('', views.habit_list, name='habit_list'),

    # Create a new habit
    path('create/', views.habit_create, name='habit_create'),

    # Edit an existing habit (by primary key)
    path('edit/<int:pk>/', views.habit_edit, name='habit_edit'),

    # Delete a habit (by primary key)
    path('delete/<int:pk>/', views.habit_delete, name='habit_delete'),

    # weekly_habit_report
    path('reports/habits/', views.weekly_habit_report, name='weekly_habit_report'),
]
