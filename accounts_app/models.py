# accounts_app/models.py

from django.db import models
from django.contrib.auth.models import User  # ✅ Using default Django User model

FREQUENCY_CHOICES = [
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Done', 'Done'),
]


class Habit(models.Model):
    # Foreign key to User
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_habits')

    # Main fields
    title = models.CharField(max_length=200)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    start_date = models.DateField()

    def __str__(self):
        # ✅ Shows both title and status properly in Django Admin
        return f"{self.title} - {self.status}"
