from django.forms import ModelForm
from .models import PriorityTask

class PriorityTaskForm(ModelForm):
    class Meta:
        model = PriorityTask
        fields = ['task1', 'task2', 'task3']

