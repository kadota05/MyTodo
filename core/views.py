from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.timezone import now
from datetime import datetime, timedelta

from PriorityTask.models import PriorityTask
from Tweet.models import Tweet

class DashboardView(TemplateView):
    template_name = "core/index.html"
    
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
        # 日付関連
        context['current_date'] = self.current_date
        context['today'] = self.today
        
        # Priority Task用
        context['task'] = PriorityTask.objects.filter(created_date=self.current_date).first()
        
        # Habit用
        
        # Tweet用
        context['tweets'] = Tweet.objects.filter(created_at=self.current_date)
        
        return context