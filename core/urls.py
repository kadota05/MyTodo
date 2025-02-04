from django.urls import path, include
from .views import DashboardView, UserLogin, UserLogout, UserRegistration, UserProfile

app_name = 'core'
urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('pre/<str:pre>/', DashboardView.as_view(), name='pre'),
    path('post/<str:post>/', DashboardView.as_view(), name='post'),
    path('select/', DashboardView.as_view(), name='select_date'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('profile/', UserProfile.as_view(), name='profile'),
    ]