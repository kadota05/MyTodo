from django.urls import path, include
from .views import HabitAdd, HabitEdit, HabitDelete, HabitLogAdd, HabitLogStatusChange, HabitLogStatusChangeView

app_name = 'Habit'
urlpatterns = [
    path('add/', HabitAdd.as_view(), name='HabitAdd'),
    path('edit/<int:pk>/', HabitEdit.as_view(), name='HabitEdit'),
    path('delete/<int:pk>/', HabitDelete.as_view(), name='HabitDelete'),
    path('logadd/<int:habit_pk>', HabitLogAdd.as_view(), name='HabitLogAdd'),
    path('logchange/<int:pk>', HabitLogStatusChange.as_view(), name='HabitLogStatusChange'),
    path('log/change/<int:pk>/', HabitLogStatusChangeView.as_view(), name='HabitLogStatusChangeView'),
    ]    