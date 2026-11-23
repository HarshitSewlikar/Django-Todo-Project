from . import views
from django.urls import path 


urlpatterns=[
    path("",views.index, name="index"),
    path("todos/",views.todo_list,name="todo_list"),
    path("create/",views.todo_create,name="todos_create"),
    path("update/",views.todo_update,name="todos_update"),
    path("delete/",views.todo_delete,name="todos_delete"),

]