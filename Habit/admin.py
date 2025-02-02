from django.contrib import admin
from .models import Habit, HabitLog

class HabitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'target_day_per_week', 'created_at']

class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'habit', 'date', 'completed', 'created_at']
    
admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitLog, HabitLogAdmin)