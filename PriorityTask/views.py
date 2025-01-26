from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from datetime import datetime, timedelta
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
            return redirect('PriorityTask:week_list')
    else:
        return redirect('PriorityTask:week_list')

def edit(request, task_id):
    if request.method == "POST":
        form = PriorityTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('PriorityTask:week_list')
    else:
        task = get_object_or_404(PriorityTask, id=task_id)
        form = PriorityTaskForm(instance=task)
        return render(request, 'PriorityTask/edit.html', {'task':task, 'form':form})

@require_POST
def delete(request, task_id):
    task = get_object_or_404(PriorityTask, id=task_id)
    task.delete()
    return redirect('PriorityTask:week_list')

def week_list(request, other_day=None):
    form = PriorityTaskForm
    
    if other_day:
        today = datetime.strptime(other_day, '%Y-%m-%d').date()
    else:
        today = now().date() # 現在時刻（now()）の日付だけ取り出す（.date()）
    
    # 一週間を日曜～土曜の周期で実装するよ
    # 日付（timedeltaを使うと自動的に年や月をまたぐ計算が実行されるから超便利！）
    start_of_week = today - timedelta(days=((today.weekday()+1) % 7)) # today.weekday()は、todayが週の何日目かを返す（月曜=0、火曜=1、…、日曜=6）
    end_of_week = start_of_week + timedelta(days=6)
    
    # 曜日
    week_days = ['日', '月', '火', '水', '木', '金', '土']
    
    # メモ
    weekly_memos = PriorityTask.objects.filter(created_date__range=[start_of_week, end_of_week])
    
    # 日付と曜日とメモを対応付ける
    date_map = []
    for i in range(7):
        date = start_of_week + timedelta(days=i)
        if date == today:
            isToday = True
        else:
            isToday = False
        weekday = week_days[i]
        memo = [memo for memo in weekly_memos if memo.created_date == date] or None # 該当するメモオブジェクトかNoneが入る
        memo = weekly_memos.filter(created_date=date).first()
        date_map.append({'date': date, 'weekday': weekday, 'memo': memo, 'isToday': isToday})
    
    return render(request, 'PriorityTask/index.html', {'date_map': date_map, 'form': form})

    