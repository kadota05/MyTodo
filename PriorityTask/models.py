from django.db import models
from django.contrib.auth.models import User

class PriorityTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='priority_tasks')
    created_date = models.DateField("作成日", auto_now_add=True)
    task1 = models.CharField("task 1", max_length=150)
    task2 = models.CharField("task 2", max_length=150)
    task3 = models.CharField("task 3", max_length=150)
    
    def __str__(self):
        return self.created_date.strftime('%y%m%d')