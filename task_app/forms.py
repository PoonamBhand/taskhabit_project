from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 3}),
            'priority': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control rounded-3'}),
        }
