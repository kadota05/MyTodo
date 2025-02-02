from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.utils.timezone import now
from datetime import timedelta, datetime
from .models import Habit, HabitLog

class HabitView(TemplateView):
    template_name = "Habit/index.html"
    
    def get(self, request, *args, **kwargs):
        self.today = now().date()
        if 'post' in kwargs:
            post = kwargs['post']
            post = datetime.strptime(post, '%Y-%m-%d').date()
            self.current_date = post + timedelta(days=1)
        elif 'pre' in kwargs:
            pre = kwargs['pre']
            pre = datetime.strptime(pre, '%Y-%m-%d').date()
            self.current_date = pre - timedelta(days=1)
        else:
            self.current_date = now().date()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        habit_data = []
        
        start_of_week = self.current_date - timedelta(days=((self.current_date.weekday()+1) % 7))
        end_of_week = start_of_week + timedelta(days=6)
        
        habits = Habit.objects.all()
        
        for habit in habits:
            weekly_logs = habit.logs.filter(date__range=[start_of_week, end_of_week])
            completed_day = weekly_logs.filter(completed=True).count()
            
            target = habit.target_day_per_week
            weekly_rate = min(int((completed_day / target) * 100), 100)
            
            # 登録日から数えてtodayまでで、何週間達成できているか
            success_weeks = 0
            creation_date = habit.created_at
            creation_week_start = creation_date - timedelta(days=((creation_date.weekday()+1) % 7))
            start_of_week_today = self.today - timedelta(days=((self.today.weekday()+1) % 7))
            # date - dateになっているから.daysで取り出す
            weeks_since_creation = (start_of_week_today - creation_week_start).days // 7
            for week in range(weeks_since_creation + 1):
                week_start = start_of_week_today - timedelta(weeks=week)
                week_end = week_start + timedelta(days=6)
                week_logs = habit.logs.filter(date__range=[week_start, week_end])
                week_completed = week_logs.filter(completed=True).count()
                if week_completed >= target:
                    success_weeks += 1
            success_weeks = min(success_weeks, 13)
            success_percentage = int((success_weeks / 13) * 100)
        
            habit_data.append({
            'habit': habit, 
            'weekly_rate': weekly_rate, 
            'completed_day': completed_day,
            'target': target,
            'success_weeks': success_weeks,
            'success_percentage': success_percentage,
            'weekly_logs': weekly_logs
            })
        
        context['habit_data'] = habit_data
        
        return context