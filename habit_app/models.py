from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ]

    GOAL_CHOICES = [
        ('Drink Water', 'Drink Water'),
        ('Exercise', 'Exercise'),
        ('Read Book', 'Read Book'),
        ('Meditate', 'Meditate'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')

    name = models.CharField(max_length=100)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    goal = models.CharField(max_length=50, choices=GOAL_CHOICES)

    def __str__(self):
        return self.name

    def streak_count(self):
        """
        Calculates how many consecutive days (or weeks) the user has completed the habit.
        """
        completions = self.habitcompletions.filter(completed=True).order_by('-date')
        if not completions.exists():
            return 0

        streak = 0
        today = timezone.now().date()
        expected_day = today

        for comp in completions:
            if comp.date == expected_day:
                streak += 1
                expected_day -= timedelta(days=1)
            else:
                break

        return streak

    def is_completed_today(self):
        """Check if the habit has been marked as completed for today."""
        today = timezone.now().date()
        return self.habitcompletions.filter(date=today, completed=True).exists()


class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="habitcompletions")
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'date')

    def __str__(self):
        return f"{self.habit.name} on {self.date} ({'Done' if self.completed else 'Pending'})"
