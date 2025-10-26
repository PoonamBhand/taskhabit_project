# habit_app/admin.py

from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'frequency', 'goal')  # ✅ show key fields
    list_filter = ('frequency', 'user')                   # optional sidebar filters
    search_fields = ('name', 'user__username')            # search bar support
