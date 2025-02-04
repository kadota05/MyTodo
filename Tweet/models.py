from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    content = models.TextField("content", max_length=500)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:20]