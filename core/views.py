from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from PriorityTask.models import PriorityTask
from Tweet.models import Tweet
from Habit.models import Habit, HabitLog

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"
    
    def get(self, request, *args, **kwargs):
        # 普通にnow()を使うとUTCの現在時刻が返されちゃうけど、timezone.localtime(now())にしたらtimezone通りの時間が得られる
        self.today = timezone.localtime(now()).date()
        if 'post' in kwargs:
            post = kwargs['post']
            post = datetime.strptime(post, '%Y-%m-%d').date()
            self.current_date = post + timedelta(days=1)
        elif 'pre' in kwargs:
            pre = kwargs['pre']
            pre = datetime.strptime(pre, '%Y-%m-%d').date()
            self.current_date = pre - timedelta(days=1)
        else:
            self.current_date = timezone.localtime(now()).date()
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.today = timezone.localtime(now()).date()
        select_data_str = request.POST.get('date')
        if select_data_str:
            try:
                self.current_date = datetime.strptime(select_data_str, '%Y-%m-%d').date()
            except ValueError:
                self.current_date = timezone.localtime(now()).date()
        else:
            self.current_date = timezone.localtime(now()).date()
        return self.render_to_response(self.get_context_data())
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 日付関連
        context['current_date'] = self.current_date
        context['today'] = self.today
        
        # Priority Task用
        context['task'] = PriorityTask.objects.filter(user=self.request.user, created_date=self.current_date).first()
        
        # Habit用
        habit_data = []
        # 現在日付を含む週の開始日（月曜始まりではなく日曜始まりの場合は計算式調整してください）
        start_of_week = self.current_date - timedelta(days=((self.current_date.weekday()+1) % 7))
        end_of_week = start_of_week + timedelta(days=6)
        
        habits = Habit.objects.filter(user=self.request.user, successful=False)
        for habit in habits:
            # 今週のログ
            weekly_logs = habit.logs.filter(date__range=[start_of_week, end_of_week])
            completed_day = weekly_logs.filter(completed=True).count()
            
            target = habit.target_day_per_week
            weekly_rate = min(int((completed_day / target) * 100), 100) if target else 0
            
            # currentdayのログ
            current_log = weekly_logs.filter(date=self.current_date).first()
            
            # 登録日から今日までの各週で、目標達成している週の数を算出
            success_weeks = 0
            creation_date = habit.created_at
            creation_week_start = creation_date - timedelta(days=((creation_date.weekday()+1) % 7))
            start_of_week_today = self.today - timedelta(days=((self.today.weekday()+1) % 7))
            weeks_since_creation = (start_of_week_today - creation_week_start).days // 7
            for week in range(weeks_since_creation + 1):
                week_start = start_of_week_today - timedelta(weeks=week)
                week_end = week_start + timedelta(days=6)
                week_logs = habit.logs.filter(date__range=[week_start, week_end])
                week_completed = week_logs.filter(completed=True).count()
                if week_completed >= target:
                    success_weeks += 1
            # 最大13週として計算
            success_weeks = min(success_weeks, 13)
            success_percentage = int((success_weeks / 13) * 100) if 13 else 0
            
            # success_percentageが100以上なら、successfulフィールドをTrueに設定
            if success_percentage >= 100:
                habit.successful = True
                habit.successful_date = self.today
                habit.save()  # 更新をデータベースに反映
            
            habit_data.append({
                'habit': habit, 
                'weekly_rate': weekly_rate, 
                'completed_day': completed_day,
                'target': target,
                'success_weeks': success_weeks,
                'success_percentage': success_percentage,
                'weekly_logs': weekly_logs,
                'current_log': current_log,
            })
        context['habit_data'] = habit_data
        
        # Tweet用
        context['tweets'] = Tweet.objects.filter(user=self.request.user, created_at=self.current_date)
        
        return context


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = 'core/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 達成済み習慣
        context['successful_habits'] = Habit.objects.filter(user=self.request.user, successful=True)
        
        # ランダムツイート
        context['past_tweet'] = Tweet.objects.filter(user=self.request.user).order_by('?').first()
        
        return context
    
    
class UserLogin(LoginView):
    template_name = 'core/user_login.html'
    redirect_authenticated_user = False
    
class UserLogout(LogoutView):
    pass

class UserRegistration(CreateView):
    form_class = UserCreationForm
    template_name = 'core/user_form.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response
