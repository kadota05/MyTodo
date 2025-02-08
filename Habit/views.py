from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Habit, HabitLog
from .forms import HabitForm

class HabitAdd(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    success_url = reverse_lazy('core:index')
    
    def get_initial(self):
        initial = super().get_initial()
        initial['created_at'] = timezone.localtime(now()).date()
        return initial
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class HabitEdit(LoginRequiredMixin, UpdateView):
    model = Habit
    form_class = HabitForm
    success_url = reverse_lazy('core:index')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    
class HabitDelete(LoginRequiredMixin, DeleteView):
    model = Habit
    success_url = reverse_lazy('core:index')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
"""
class HabitLogAdd(LoginRequiredMixin, CreateView):
    model = HabitLog
    fields = []
    success_url = reverse_lazy('core:index')
    
    def get(self, request, *args, **kwargs):
        habit_pk = self.kwargs.get('habit_pk')
        habit = Habit.objects.get(pk=habit_pk, user=self.request.user)
        
        self.object = HabitLog.objects.create(
            habit=habit,
            date=timezone.localtime(now()).date(),
            completed=True,
        )
        return HttpResponseRedirect(self.success_url)
"""

class HabitLogAdd(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        habit_pk = self.kwargs.get('habit_pk')
        habit = get_object_or_404(Habit, pk=habit_pk, user=request.user)
        
        # 当日のログが既に存在していないかチェックする（必要に応じて）
        if not HabitLog.objects.filter(habit=habit, date=timezone.localtime(now()).date()).exists():
            habit_log = HabitLog.objects.create(
                habit=habit,
                date=timezone.localtime(now()).date(),
                completed=True,
            )
        # JSONレスポンスを返す（リダイレクトの場合は非同期側でリロードなどの処理が必要）
        return JsonResponse({'success': True})

class HabitLogStatusChange(LoginRequiredMixin, UpdateView):
    model = HabitLog
    success_url = reverse_lazy('core:index')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.completed = not self.object.completed
        self.object.save(update_fields=["completed"])
        return HttpResponseRedirect(self.success_url)
    
class HabitLogStatusChangeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # 対象のHabitLogの状態をトグル
        habit_log = get_object_or_404(HabitLog, id=pk, habit__user=request.user)
        habit_log.completed = not habit_log.completed
        habit_log.save()
        
        # 更新対象のHabitを取得
        habit = habit_log.habit
        current_date = timezone.localtime(now()).date()
        # 今週の開始・終了日（例：日曜始まり）
        start_of_week = current_date - timedelta(days=((current_date.weekday()+1) % 7))
        end_of_week = start_of_week + timedelta(days=6)
        weekly_logs = habit.logs.filter(date__range=[start_of_week, end_of_week])
        completed_day = weekly_logs.filter(completed=True).count()
        target = habit.target_day_per_week
        weekly_rate = min(int((completed_day / target) * 100), 100) if target else 0
        
        # 習慣化率の計算（過去の各週で目標を達成している週の数）
        success_weeks = 0
        creation_date = habit.created_at
        creation_week_start = creation_date - timedelta(days=((creation_date.weekday()+1) % 7))
        start_of_week_today = current_date - timedelta(days=((current_date.weekday()+1) % 7))
        weeks_since_creation = (start_of_week_today - creation_week_start).days // 7
        for week in range(weeks_since_creation + 1):
            week_start = start_of_week_today - timedelta(weeks=week)
            week_end = week_start + timedelta(days=6)
            week_logs = habit.logs.filter(date__range=[week_start, week_end])
            week_completed = week_logs.filter(completed=True).count()
            if week_completed >= target:
                success_weeks += 1
        success_weeks = min(success_weeks, 13)
        success_percentage = int((success_weeks / 13) * 100) if 13 else 0
        
        return JsonResponse({
            'success': True,
            'completed': habit_log.completed,
            'weekly_rate': weekly_rate,
            'completed_day': completed_day,
            'target': target,
            'success_weeks': success_weeks,
            'success_percentage': success_percentage,
            'habit_id': habit.id,
        })