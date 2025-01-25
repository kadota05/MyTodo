from django.urls import path, include
from .views import index, edit, add, delete, week_list

app_name = 'PriorityTask'
urlpatterns = [
    path('', week_list, name='week_list'),
    path('edit/<int:task_id>/', edit, name='edit'),
    path('add/', add, name='add'),
    path('delete/<int:task_id>/', delete, name='delete')
]