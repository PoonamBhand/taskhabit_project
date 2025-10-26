from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from task_app.models import Task
from habit_app.models import Habit
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth import login

from habit_app.models import Habit


# ----------------- Admin Dashboard -----------------
@staff_member_required
def admin_dashboard(request):
    users = User.objects.all()

    # Prepare list of users with task & habit counts
    users_data = []
    for user in users:
        total_tasks = Task.objects.filter(user=user).count()
        total_habits = Habit.objects.filter(user=user).count()
        users_data.append({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'total_tasks': total_tasks,
            'total_habits': total_habits,
            'is_active': user.is_active,
        })

    context = {
        'users_data': users_data,
        'total_users': users.count(),
        'total_tasks': Task.objects.count(),
        'total_habits': Habit.objects.count(),
        'blocked_users_count': users.filter(is_active=False).count(),
    }
    return render(request, 'accounts_app/admin_dashboard.html', context)

# ----------------- Block / Unblock User -----------------
@staff_member_required
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, "Cannot block superuser!")
        return redirect('admin_dashboard')
    user.is_active = False
    user.save()
    messages.success(request, f"{user.username} has been blocked.")
    return redirect('admin_dashboard')

@staff_member_required
def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"{user.username} has been activated.")
    return redirect('admin_dashboard')

# ----------------- User Dashboard -----------------
def user_dashboard(request):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    weekly_tasks = Task.objects.filter(user=request.user, due_date__range=[week_start, week_end])
    tasks_per_day = {
        (week_start + timedelta(days=i)).strftime("%A"): weekly_tasks.filter(
            due_date=week_start + timedelta(days=i),
            status='Done'
        ).count() for i in range(7)
    }

    habits = Habit.objects.filter(user=request.user)
    habits_data = {}
    for habit in habits:
        total_days = (today - habit.start_date).days + 1
        completed_days = habit.completed_days.count()  # ManyToMany for completed days
        habits_data[habit.name] = round((completed_days / total_days) * 100, 1) if total_days > 0 else 0

    context = {
        'tasks_per_day': tasks_per_day,
        'habits_data': habits_data
    }
    return render(request, 'accounts_app/user_dashboard.html', context)

# ----------------- Signup / Login / Logout -----------------
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup (optional)
            messages.success(request, "Account created successfully!")
            return redirect("dashboard")  # redirect to user dashboard
    else:
        form = SignUpForm()
    return render(request, "accounts_app/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect("admin_dashboard")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "accounts_app/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

# ----------------- Profile / User Details -----------------
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    tasks = Task.objects.filter(user=request.user)
    habits = Habit.objects.filter(user=request.user)
    return render(request, "accounts_app/profile.html", {"user": request.user, "tasks": tasks, "habits": habits})

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(user=user)
    habits = Habit.objects.filter(user=user)
    return render(request, 'accounts_app/user_detail.html', {'user': user, 'tasks': tasks, 'habits': habits})

def user_tasks(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(user=user)
    return render(request, 'accounts_app/user_tasks.html', {'user': user, 'tasks': tasks})

def user_habits(request, user_id):
    user = get_object_or_404(User, id=user_id)
    habits = Habit.objects.filter(user=user)
    return render(request, 'accounts_app/user_habits.html', {'user': user, 'habits': habits})

def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_dashboard')

def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_dashboard')

def weekly_task_report(request):
    today = timezone.now().date()
    last_week = today - timedelta(days=6)  # last 7 days
    report_data = []

    for i in range(7):
        day = last_week + timedelta(days=i)
        completed_tasks = Task.objects.filter(
            due_date=day,
            status='Done'
        ).count()
        report_data.append({'date': day.strftime("%b %d"), 'completed': completed_tasks})

    return render(request, 'reports/weekly_task_report.html', {'report_data': report_data})

def habit_performance_report(request):
    habits = Habit.objects.all()
    performance_data = []

    for habit in habits:
        total_days = habit.total_days() if hasattr(habit, 'total_days') else 1
        completed_days = habit.completed_days() if hasattr(habit, 'completed_days') else 0
        percentage = int((completed_days / total_days) * 100) if total_days else 0
        streak = habit.current_streak() if hasattr(habit, 'current_streak') else 0
        performance_data.append({
            'habit': habit.name,
            'percentage': percentage,
            'streak': streak
        })

    return render(request, 'reports/weekly_habit_report.html', {'performance_data': performance_data})


def habits_view(request):
    habits = Habit.objects.filter(user=request.user)
    context = {
        'habits': habits,
        'active_tab': 'habits',
    }
    return render(request, 'tasks.html', context)
