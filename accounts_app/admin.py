# accounts_app/admin.py

from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class AccountHabitAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'frequency', 'status')  # ✅ show data properly
    list_filter = ('frequency', 'status')                    # optional filters
    search_fields = ('title', 'user__username')              # search bar
