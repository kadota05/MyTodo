from django.db import models

class Tweet(models.Model):
    content = models.TextField("内容", max_length=500)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:20]