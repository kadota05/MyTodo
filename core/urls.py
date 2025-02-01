from django.urls import path, include
from .views import DashboardView

app_name = 'core'
urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('pre/<str:pre>/', DashboardView.as_view(), name='pre'),
    path('post/<str:post>/', DashboardView.as_view(), name='post'),
    ]