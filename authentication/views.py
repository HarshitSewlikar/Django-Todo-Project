from django.shortcuts import render

# Create your views here.
import json
from json import JSONDecodeError
from django.http import HttpResponse, JsonResponse


from django.middleware.csrf import get_token#imported to get teh csrf tokken 
from django.views.decorators.csrf import ensure_csrf_cookie#imported to get ensure csrf cookie 
from django.views.decorators.http import require_GET#ensure that get method is used to get cookie

@require_GET#decorator extend the functionaily of the previous written function
@ensure_csrf_cookie#also decorator

def get_csrf_token(request):#function to get the csrf token
    token = get_token(request)

    return JsonResponse({
        'csrf_token':token
    })


#login page 

from django.views.decorators.http import require_POST

from django.contrib.auth import authenticate , login
@require_POST
def todo_login(request):
       try:
        data = json.loads(request.body)
       except JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"},status=400)
       username = data.get("username")
       password = data.get("password")

       user = authenticate(request,username=username,password=password)
       if user is None:
         return JsonResponse({"error":"Invalid username or password"},status=401)
        
       login(request,user)
       return JsonResponse({"username": user.username,"id": user.id})

#register page 

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError


User = get_user_model()
@require_POST
def todo_register(request):
   try:
    data = json.loads(request.body)
   except JSONDecodeError:
    return JsonResponse({"error": "Invalid JSON"},status=400)
   username = data.get("username")
   email = data.get("email")
   password = data.get("password")
   try:
        validate_password(password)
   except ValidationError:
        return JsonResponse({"error": "Invalid password"},status=400)
   
   try:
    user = User.objects.create_user(username=username,email=email,password=password)
   except IntegrityError:
      return JsonResponse({"error": "Username already exists"},status=400)
   return JsonResponse({"username": user.username,"id": user.id})

#logout page 

from django.contrib.auth import logout
@require_POST
def todo_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})