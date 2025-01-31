from django.db import models

class PriorityTask(models.Model):
    created_date = models.DateField("作成日", auto_now_add=True)
    task1 = models.CharField("タスク1", max_length=150)
    task2 = models.CharField("タスク2", max_length=150)
    task3 = models.CharField("タスク3", max_length=150)
    
    def __str__(self):
        return self.created_date.strftime('%y%m%d')