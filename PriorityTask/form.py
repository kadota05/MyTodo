from django import forms
from django.forms import ModelForm
from .models import PriorityTask

class PriorityTaskForm(ModelForm):
    class Meta:
        model = PriorityTask
        fields = ['task1', 'task2', 'task3']
        widgets = {
            'task1': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'task2': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'task3': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }
