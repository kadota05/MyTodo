from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .form import TweetForm
from .models import Tweet

class add(CreateView):
    model = Tweet
    form_class = TweetForm
    success_url = reverse_lazy('core:index')
    
class delete(DeleteView):
    model = Tweet
    success_url = reverse_lazy('core:index')