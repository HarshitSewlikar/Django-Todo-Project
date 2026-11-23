from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.password_validation import validate_password
# Create your views here.

def index(request):#just did an view and url connected check not for code
    return HttpResponse("Hello, world. You're at the todos index.")


from .models import Todo #create an todo name class in models.py and imported that here

def todo_list(request):#code for list the todo getting it all from the db
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    todos = Todo.objects.filter(user=request.user)
    data = [{'id':t.id,'title':t.title,'description':t.description,'status':t.status} for t in todos]
    return JsonResponse(data,safe=False)





import json #needed in order to load the put data from postman
from json import JSONDecodeError
from django.views.decorators.http import require_POST

#code for creating new todo record 
@require_POST
def todo_create(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    try:
      data = json.loads(request.body)
      if not isinstance(data,dict):
        return JsonResponse({"error": "Invalid data"},status=400)
      
      
      title = data.get('title')
      if isinstance(title, str):
        title = title.strip()
      else:
        return JsonResponse({"error": "Invalid data"},status=400)
      
      
      description=data.get('description',"")
      if isinstance(description,str):
        description = description.strip()
      else:
        return JsonResponse({"error": "Invalid data"},status=400)
      
      
      status=data.get('status',"OPEN")
      if isinstance(status,str):
        status = status.strip().upper()
        if status not in {"OPEN", "IN_PROGRESS", "COMPLETED"}:
           return JsonResponse({"error": "Invalid status"}, status=400)
      else:
        return JsonResponse({"error": "Invalid data"},status=400)
      
      
      if not title :
        return JsonResponse({"error": "Invalid data"},status=400)
    
    
    except JSONDecodeError:
        return JsonResponse({"error": "Invalid data"},status=400)
    
    todo = Todo.objects.create(user=request.user,title=title,description=description,status=status)
    response_data ={'id':todo.id,'title':todo.title,'description':todo.description,'status':todo.status}
    return JsonResponse(response_data,status=201)


#code for update todo
from django.views.decorators.http import require_http_methods


@require_http_methods(["PUT","PATCH"])
def todo_update(request):#creating an update function
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    try:
     
     data = json.loads(request.body)
     if not isinstance(data,dict):
      return JsonResponse({"error":"Invalid data"},status=400)
       
    except JSONDecodeError:
      return JsonResponse({"error":"Invalid data"},status=400)
      
      
    try:
       ide = data.get('id')
       if not isinstance(ide,int):
        return JsonResponse({"error":"Invalid data"},status=400)
       todo = Todo.objects.get(id=ide,user=request.user)
       

    except Todo.DoesNotExist:
      return JsonResponse({"error":"Todo not found"},status=404)

    

      
      

    if request.method == "PUT":

      
       title=data.get('title')
       if isinstance(title,str):
        title = title.strip()
       else:
        return JsonResponse({"error":"Invalid data"},status=400)
       if not title:
          return JsonResponse({"error":"Invalid data"},status=400)
       
       description=data.get('description')
       if isinstance(description,str):
        description = description.strip()
       else:
        return JsonResponse({"error":"Invalid data"},status=400)
       status=data.get('status')
       if isinstance(status,str):
        status = status.strip().upper()
        if status not in {"OPEN", "IN_PROGRESS", "COMPLETED"}:
          return JsonResponse({"error":"Invalid status"},status=400)
       else:
        return JsonResponse({"error":"Invalid data"},status=400)
       

       todo.title =  title
       todo.description = description
       todo.status = status

    else:
      if "title" in data:
        title = data.get('title')
        if isinstance(title,str):
          title = title.strip()
        else:
          return JsonResponse({"error":"Invalid data"},status=400)
        if not title:
          return JsonResponse({"error":"Invalid data"},status=400)
        todo.title = title
     
      if "description" in data:
        description = data.get('description')
        if isinstance(description,str):
          description = description.strip()
        else:
          return JsonResponse({"error":"Invalid data"},status=400)
        todo.description = description
      
      if "status" in data:
        status = data.get('status')
        if isinstance(status,str):
          status = status.strip().upper()
        else:
          return JsonResponse({"error":"Invalid data"},status=400)
        if status not in {"OPEN", "IN_PROGRESS", "COMPLETED"}:
          return JsonResponse({"error":"Invalid status"},status=400)
        todo.status = status
    
    todo.save()
    response_data ={"id":todo.id,"title":todo.title,"description":todo.description,"status":todo.status}
    return JsonResponse(response_data)

#code for delete todo
from django.views.decorators.http import require_http_methods
@require_http_methods(["DELETE"])
def todo_delete(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    try:
      data =json.loads(request.body)
      if not isinstance(data,dict):
        return JsonResponse({"error":"Invalid data"},status=400)
    except JSONDecodeError:
      return JsonResponse({"error":"Invalid data"},status=400)
     
      
    ide = data.get("id")
      
    if not isinstance(ide,int):
      return JsonResponse({"error":"Invalid data"},status=400)


    try:
      todos = Todo.objects.get(id=ide,user=request.user)
    except Todo.DoesNotExist:
        return JsonResponse({"error":"Todo not Found"},status=404)

    todos.delete()
    
    return JsonResponse({"deleted": ide})
    

    

