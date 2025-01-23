from django.contrib import admin
from .models import PriorityTask

class PriorityTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_date', 'task1', 'task2', 'task3']
    list_display_url = ['id']

admin.site.register(PriorityTask, PriorityTaskAdmin)