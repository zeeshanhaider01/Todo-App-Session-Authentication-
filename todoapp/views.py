from django.contrib.auth.models import User
# from django.http import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer

# Create your views here.
@api_view(["POST"])
def user_signup(request):
    if request.method == "POST":
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error":"Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"error":"Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return Response({"message":"User Successfully Created"}, status=status.HTTP_201_CREATED)

    else:
        return Response({"error":"Invalid request method. Use Post method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["POST"])
def login_view(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return Response({"message":"Login Successful"},status=status.HTTP_200_OK)

        else:
            return Response({"error":"Invalid username or password"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"error":"Invalid request method. Use Post method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required(login_url="login/")
@api_view(["GET", "POST"])
def todo_list(request):
    if request.method ==  "GET":
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url="login/")
@api_view(["GET", "PATCH", "PUT", "DELETE"])
def todo_detail(request, pk):
    print(f"##############Request user: {request.user}")  # Debug
    print(f"##############Todo ID: {pk}")
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    
    if request.method == 'GET':
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos,many=True)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        todo.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    