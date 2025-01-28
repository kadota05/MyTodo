from django.urls import path, include
from .views import index, edit, add, delete

app_name = 'PriorityTask'
urlpatterns = [
    path('', index.as_view(), name='index'),
    path('pre/<str:pre>/', index.as_view(), name='pre'),
    path('post/<str:post>/', index.as_view(), name='post'),
    path('add/', add.as_view(), name='add'),
    path('edit/<int:pk>/', edit.as_view(), name='edit'),
    path('delete/<int:pk>/', delete.as_view(), name='delete'),
]