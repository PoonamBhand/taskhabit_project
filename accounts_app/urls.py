from django.urls import path
from . import views

urlpatterns = [
    # Admin Dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Authentication
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # User Profile
    path("profile/", views.profile_view, name="profile"),

    # User-specific pages (make sure these views exist)
    path('user/<int:user_id>/', views.user_detail, name="user_detail"),
    path('user/<int:user_id>/tasks/', views.user_tasks, name='user_tasks'),
    path('user/<int:user_id>/habits/', views.user_habits, name='user_habits'),


    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),

    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),

    path('reports/tasks/', views.weekly_task_report, name='weekly_task_report'),
    path('reports/habits/', views.habit_performance_report, name='habit_performance_report'),

]
