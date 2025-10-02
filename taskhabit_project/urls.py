from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts_app.urls')),
    path('tasks/', include('task_app.urls')),
    path('habits/', include('habit_app.urls')),
]
