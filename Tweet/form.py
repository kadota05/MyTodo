from django import forms
from django.forms import ModelForm
from .models import Tweet

class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
        }