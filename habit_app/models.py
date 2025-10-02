from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=200)
    frequency = models.CharField(max_length=50, choices=[('Daily','Daily'), ('Weekly','Weekly')])
    goal = models.IntegerField(default=1)  # e.g. times per day/week
    group = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from django.db import models

# Create your models here.
