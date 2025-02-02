from django import forms
from django.forms import ModelForm
from .models import Habit

class HabitForm(ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'target_day_per_week', 'created_at']
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'}),
        }
