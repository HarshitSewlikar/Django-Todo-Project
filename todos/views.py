from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

def index(request):#just did an view and url connected check not for code
    return HttpResponse("Hello, world. You're at the todos index.")


from .models import Todo #create an todo name class in models.py and imported that here

def todo_list(request):#code for llist the todo getting it all from the db
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    todos = Todo.objects.all().filter(user=request.user)
    data = [{'id':t.id,'title':t.title,'description':t.description,'status':t.status} for t in todos]
    return JsonResponse(data,safe=False)


import json#needed in order to load the put data from postman

def todo_create(request):#code for creating new todo record 
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    data = json.loads(request.body)
    title = data.get('title')
    description=data.get('description')
    status=data.get('status')
    Todo.objects.create(user=request.user,title=title,description=description,status=status)
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
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    data = json.loads(request.body)
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')
    ide = data.get('id')
    todo = Todo.objects.get(id=ide,user=request.user)
    todo.title = title
    todo.description = description
    todo.status = status
    todo.save()
    return JsonResponse(data,safe=False)

#code for delete todo
def todo_delete(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    data =json.loads(request.body)
    ide = data.get("id")
    todos = Todo.objects.get(id=ide,user=request.user)
    todos.delete()
    return JsonResponse({"deleted": ide})
    

    #login page 

from django.contrib.auth import authenticate , login

def todo_login(request):
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request,username=username,password=password)
        if user is None:
            return JsonResponse({"error":"Invalid username or password"},status=401)
        
        login(request,user)
        return JsonResponse({"username": user.username,"id": user.id})

#register page 

from django.contrib.auth import get_user_model

User = get_user_model()

def todo_register(request):
    data = json.loads(request.body)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    user = User.objects.create_user(username=username,email=email,password=password)
    return JsonResponse({"username": user.username,"id": user.id})

#logout page 
from django.contrib.auth import logout
def todo_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})