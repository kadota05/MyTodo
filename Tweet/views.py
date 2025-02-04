from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .form import TweetForm
from .models import Tweet

class add(LoginRequiredMixin, CreateView):
    model = Tweet
    form_class = TweetForm
    success_url = reverse_lazy('core:index')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class delete(LoginRequiredMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy('core:index')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)