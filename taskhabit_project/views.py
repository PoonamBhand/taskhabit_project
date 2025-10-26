from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from task_app.models import Task
from habit_app.models import Habit, HabitCompletion


@login_required
def dashboard(request):
    today = timezone.now().date()


    # Tasks due today (only pending ones)
    today_tasks = Task.objects.filter(user=request.user, due_date=today, status="Pending")

    # Habits not yet completed today
    habits = Habit.objects.filter(user=request.user)
    incomplete_habits = [
        h for h in habits if not HabitCompletion.objects.filter(habit=h, date=today).exists()
    ]

    # Weekly task summary
    week_start = today - timedelta(days=today.weekday())   # Monday
    week_end = week_start + timedelta(days=6)              # Sunday
    week_tasks = Task.objects.filter(user=request.user, due_date__range=[week_start, week_end])

    completed = week_tasks.filter(status="Done").count()
    pending = week_tasks.filter(status="Pending").count()

    context = {
        "today_tasks": today_tasks,
        "incomplete_habits": incomplete_habits,
        "completed": completed,
        "pending": pending,
    }
    return render(request, "dashboard.html", context)
