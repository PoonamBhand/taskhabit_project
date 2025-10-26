from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from habit_app.models import Habit

from habit_app.models import Habit
from .models import Task
from .forms import TaskForm
# -------------------
# List Tasks
# -------------------
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_app/task_list.html', {'tasks': tasks})


# -------------------
# Create Task
# -------------------
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.status = 'Pending'  # ✅ set automatically
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_app/task_form.html', {'form': form})



# -------------------
# Edit Task
# -------------------
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_app/task_form.html', {'form': form})


# -------------------
# Delete Task
# -------------------
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_app/task_confirm_delete.html', {'task': task})


# -------------------
# Toggle Status
# -------------------
@login_required
def task_toggle_status(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.status == 'Pending':
        task.status = 'Done'
    else:
        task.status = 'Pending'
    task.save()
    return redirect('task_list')


# -------------------
# Dashboard
# -------------------
@login_required
def dashboard(request):
    user = request.user
    today = timezone.localdate()

    # Tasks belonging to this user
    user_tasks = Task.objects.filter(user=user)

    # 1️⃣ Today's Pending Tasks
    todays_pending = user_tasks.filter(due_date=today, status="Pending")

    # 2️⃣ Habits for today
    todays_habits = Habit.objects.filter(user=user, frequency__in=["Daily", "Weekly", "Monthly"])

    # 3️⃣ Weekly Summary
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    weekly_tasks = user_tasks.filter(due_date__range=[start_of_week, end_of_week])
    completed_count = weekly_tasks.filter(status="Done").count()
    pending_count = weekly_tasks.filter(status="Pending").count()

    context = {
        "todays_pending": todays_pending,
        "todays_habits": todays_habits,
        "completed_count": completed_count,
        "pending_count": pending_count,
    }
    return render(request, "task_app/dashboard.html", context)

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

    return render(request, 'reports_app/weekly_task_report.html', {'report_data': report_data})
