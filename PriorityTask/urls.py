from django.urls import path, include
from .views import WeekView, edit, add, delete

app_name = 'PriorityTask'
urlpatterns = [
    path('', WeekView.as_view(), name='week_list'),
    path('other/<str:other_date>/', WeekView.as_view(), name='other_date'),
    path('add/', add.as_view(), name='add'),
    path('edit/<int:pk>/', edit.as_view(), name='edit'),
    path('delete/<int:pk>/', delete.as_view(), name='delete'),
]