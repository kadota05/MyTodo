from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import PriorityTask
from .form import PriorityTaskForm

def index(request):
    tasks = PriorityTask.objects.all()
    form = PriorityTaskForm
    return render(request, 'PriorityTask/index.html', {'tasks': tasks, 'form': form})

def add(request):
    if request.method == "POST":
        form = PriorityTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('PriorityTask:index')
    else:
        return redirect('PriorityTask:index')

def edit(request, task_id):
    if request.method == "POST":
        form = PriorityTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('PriorityTask:index')
    else:
        task = get_object_or_404(PriorityTask, id=task_id)
        form = PriorityTaskForm(instance=task)
        return render(request, 'PriorityTask/edit.html', {'task':task, 'form':form})

@require_POST
def delete(request, task_id):
    task = get_object_or_404(PriorityTask, id=task_id)
    task.delete()
    return redirect('PriorityTask:index')