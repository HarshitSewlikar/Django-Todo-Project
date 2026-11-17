from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

def index(request):#just did an view and url connected check not for code
    return HttpResponse("Hello, world. You're at the todos index.")


from .models import Todo #create an todo name class in models.py and imported that here

def todo_list(request):#code for llist the todo getting it all from the db
    todos = Todo.objects.all()
    data = [{'id':t.id,'title':t.title,'description':t.description,'status':t.status} for t in todos]
    return JsonResponse(data,safe=False)


import json#needed in order to load the put data from postman

def todo_create(request):#code for creating new todo record 
    data = json.loads(request.body)
    title = data.get('title')
    description=data.get('description')
    status=data.get('status')
    Todo.objects.create(title=title,description=description,status=status)
    return JsonResponse(data,safe=False)

from django.middleware.csrf import get_token#imported to get teh csrf tokken 
from django.views.decorators.csrf import ensure_csrf_cookie#imported to get ensure csrf cookie 
from django.views.decorators.http import require_GET#ensure that get method is used to get cookie

@require_GET#decorator extend the functionaily of the previous written function
@ensure_csrf_cookie#also decorator

def get_csrf_token(request):#function to get the csrf token
    token=get_token(request)

    return JsonResponse({
        'csrf_token':token
    })
    

#code for update todo
def todo_update(request):#creating an update function
    data = json.loads(request.body)
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')
    ide = data.get('id')
    todo = Todo.objects.get(id=ide)
    todo.title = title
    todo.description = description
    todo.status = status
    todo.save()
    return JsonResponse(data,safe=False)

#code for delete todo
def todo_delete(request):
    data =json.loads(request.body)
    ide = data.get("id")
    todos = Todo.objects.get(id=ide)
    todos.delete()
    