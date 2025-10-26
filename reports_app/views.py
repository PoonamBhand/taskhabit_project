from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from task_app.models import Task
from habit_app.models import Habit, HabitCompletion
from django.contrib.auth.decorators import login_required

@login_required
def weekly_task_report(request):
    today = timezone.now().date()
    last_week_start = today - timedelta(days=6)

    report_data = []
    for i in range(7):
        day = last_week_start + timedelta(days=i)
        completed_tasks = Task.objects.filter(due_date=day, status='Done').count()
        report_data.append({'date': day.strftime("%a %d %b"), 'completed': completed_tasks})

    return render(request, 'reports_app/weekly_task_report.html', {'report_data': report_data})

@login_required
def weekly_habit_report(request):
    today = timezone.now().date()
    last_week_start = today - timedelta(days=6)

    report_data = []
    for i in range(7):
        day = last_week_start + timedelta(days=i)
        # Count habit completions for that day
        completed_habits = HabitCompletion.objects.filter(date=day, completed=True).count()
        report_data.append({'date': day.strftime("%a %d %b"), 'completed': completed_habits})

    return render(request, 'reports_app/weekly_habit_report.html', {'report_data': report_data})
    return render(request, 'reports_app/weekly_task_report.html', {'report_data': report_data})
