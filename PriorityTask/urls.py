from django.urls import path, include
from .views import edit, add, delete

app_name = 'PriorityTask'
urlpatterns = [
    path('add/', add.as_view(), name='add'),
    path('edit/<int:pk>/', edit.as_view(), name='edit'),
    path('delete/<int:pk>/', delete.as_view(), name='delete'),
]