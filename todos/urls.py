from . import views
from django.urls import path 

urlpatterns=[
    path("",views.index, name="index"),
    path("todos/",views.todo_list,name="todo_list"),
    path("csrf/",views.get_csrf_token,name="get_csrf_token"),
    path("create/",views.todo_create,name="todos_create"),
    path("update/",views.todo_update,name="todos_update"),
    path("delete/",views.todo_delete,name="todos_delete"),
    path("login/",views.todo_login,name="todo_login"),
    path("register/",views.todo_register,name="todo_register"),
    path("logout/",views.todo_logout,name="todo_logout"),
]