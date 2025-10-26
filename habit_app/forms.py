from django import forms
from .models import Habit

GOAL_CHOICES = [
    ('Read Book', 'Read Book'),
    ('Drink Water', 'Drink Water'),
    ('Exercise', 'Exercise'),
    ('Other', 'Other'),
]


class HabitForm(forms.ModelForm):
    goal = forms.ChoiceField(choices=GOAL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Habit
        fields = ['name', 'frequency', 'goal']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
        }
