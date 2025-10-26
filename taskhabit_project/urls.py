from django.contrib import admin
from django.urls import path, include
from task_app.views import dashboard, task_list, task_create, task_edit, task_delete, task_toggle_status
from task_app import views

# If you want dashboard in accounts_app for login-required:
from django.contrib.auth.decorators import login_required

# Wrap dashboard with login_required
dashboard = login_required(dashboard)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page → dashboard
    path('', dashboard, name='dashboard'),

    # Task app URLs
    path('tasks/', task_list, name='task_list'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/edit/<int:pk>/', task_edit, name='task_edit'),
    path('tasks/delete/<int:pk>/', task_delete, name='task_delete'),
    path('tasks/toggle/<int:pk>/', task_toggle_status, name='task_toggle_status'),
    # Include apps URLs (if you have separate urls.py in apps)
    path('habits/', include('habit_app.urls')),
    path('accounts/', include('accounts_app.urls')),
    path('tasks/', include('task_app.urls')),
    path('reports/tasks/', views.weekly_task_report, name='weekly_task_report'),
    path('reports/', include('reports_app.urls')),

]
