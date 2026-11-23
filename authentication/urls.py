from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.get_csrf_token, name='get_csrf_token'),
    path('login/', views.todo_login, name='todo_login'),
    path('register/',views.todo_register, name='todo_register'),
    path('logout/', views.todo_logout, name='todo_logout'),
]