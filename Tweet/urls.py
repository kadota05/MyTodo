from django.urls import path
from .views import add, delete

app_name = 'Tweet'
urlpatterns = [
    path("add/", add.as_view(), name='add'),
    path("delete/<int:pk>", delete.as_view(), name='delete')
]