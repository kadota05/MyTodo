from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField("habit name", max_length=100)
    target_day_per_week = models.PositiveIntegerField("times per week", default=3, validators=[MaxValueValidator(7)])
    successful = models.BooleanField("successful", default=False)
    successful_date = models.DateField("successful date", null=True, blank=True)
    created_at = models.DateField("created date")
    
    def __str__(self):
        return self.name

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField("作成")
    completed = models.BooleanField("達成", default=False)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    
    class Meta:
        unique_together = ('habit', 'date')
        
    def __str__(self):
        status = "達成" if self.completed else "未達成"
        return f"{self.habit.name} - {self.date} : {status}"