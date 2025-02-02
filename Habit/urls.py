from django.urls import path, include
from .views import HabitView

app_name = 'Habit'
urlpatterns = [
    path('', HabitView.as_view(), name='index'),
    path('pre/<str:pre>/', HabitView.as_view(), name='pre'),
    path('post/<str:post>/', HabitView.as_view(), name='post'),
    
    ]