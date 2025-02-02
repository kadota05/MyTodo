from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Habit, HabitLog
from .forms import HabitForm

class HabitAdd(CreateView):
    model = Habit
    form_class = HabitForm
    success_url = reverse_lazy('core:index')
    
    def get_initial(self):
        initial = super().get_initial()
        initial['created_at'] = now().date()
        return initial
    
class HabitEdit(UpdateView):
    model = Habit
    form_class = HabitForm
    success_url = reverse_lazy('core:index')
    
class HabitDelete(DeleteView):
    model = Habit
    success_url = reverse_lazy('core:index')
    
class HabitLogAdd(CreateView):
    model = HabitLog
    success_url = reverse_lazy('core:index')
    
    def get(self, request, *args, **kwargs):
        habit_pk = self.kwargs.get('habit_pk')
        habit = Habit.objects.get(pk=habit_pk)
        
        self.object = HabitLog.objects.create(
            habit=habit,
            date=now().date(),
            completed=True,
        )
        return HttpResponseRedirect(self.success_url)

class HabitLogStatusChange(UpdateView):
    model = HabitLog
    success_url = reverse_lazy('core:index')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.completed = not self.object.completed
        self.object.save(update_fields=["completed"])
        return HttpResponseRedirect(self.success_url)