from django.urls import path, include
from .views import index, edit, add, delete

app_name = 'PriorityTask'
urlpatterns = [
    path('', index, name='index'),
    path('edit/<int:task_id>/', edit, name='edit'),
    path('add/', add, name='add'),
    path('delete/<int:task_id>/', delete, name='delete')
]