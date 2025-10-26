from django.shortcuts import render, redirect
from .forms import HabitForm
from .models import Habit, HabitCompletion
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HabitForm
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from .models import Habit  # make sure your Habit model is imported


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habit_app/habit_list.html', {'habits': habits})

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)   # don’t save yet
            habit.user = request.user         # assign logged-in user
            habit.save()                      # now save
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'habit_app/habit_form.html', {'form': form})


def habit_edit(request, pk):
    habit = Habit.objects.get(pk=pk)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habit_app/habit_form.html', {'form': form})

def habit_delete(request, pk):
    habit = Habit.objects.get(pk=pk)
    if request.method == 'POST':
        habit.delete()
        return redirect('habit_list')
    return render(request, 'habit_app/habit_confirm_delete.html', {'habit': habit})


def weekly_habit_report(request):
    today = timezone.now().date()
    last_week = today - timedelta(days=6)
    report_data = []

    for i in range(7):
        day = last_week + timedelta(days=i)
        completed_habits = HabitCompletion.objects.filter(
            date=day,
            completed=True
        ).count()
        report_data.append({'date': day.strftime("%b %d"), 'completed': completed_habits})

    return render(request, 'reports_app/weekly_habit_report.html', {'report_data': report_data})
