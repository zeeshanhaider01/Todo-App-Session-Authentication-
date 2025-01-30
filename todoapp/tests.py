from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Todo


# Create your tests here.
class UserSignupTests(APITestCase):
    def test_user_signup_success(self):
        data = {"username": "testuser", "email": "testuser@example.com", "password": "password123"}
        response = self.client.post("/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User Successfully Created")
    
    def test_user_signup_duplicate_username(self):
        User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")
        data = {"username": "testuser", "email": "test2@example.com", "password": "password123"}
        response = self.client.post("/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username already taken")
    
    def test_user_signup_duplicate_email(self):
        User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")
        data = {"username": "testuser2", "email": "testuser@example.com", "password": "password123"}
        response = self.client.post("/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Email already exists")

class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")
    
    def test_login_success(self):
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login Successful")
    
    def test_login_invalid_credentials(self):
        data = {"username": "wronguser", "password": "wrongpassword"}
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid username or password")

class TodoListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)  # Log in the user
    
    def test_get_todo_list(self):
        Todo.objects.create(user=self.user, task="Task 1", completed=False)
        Todo.objects.create(user=self.user, task="Task 2", completed=True)
        response = self.client.get("/todos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_create_todo(self):
        data = {"task": "New Task", "completed": False}
        response = self.client.post("/todos/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["task"], "New Task")

class TodoDetailTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.todo = Todo.objects.create(user=self.user, task="Sample Task", completed=False)
        self.client.force_authenticate(user=self.user)
    
    def test_get_todo_detail(self):
        response = self.client.get(f"/todos/{self.todo.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["task"], "Sample Task")
    
    def test_update_todo(self):
        data = {"task": "Updated Task", "completed": True}
        response = self.client.patch(f"/todos/{self.todo.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.task, "Updated Task")
        self.assertTrue(self.todo.completed)
    
    def test_delete_todo(self):
        response = self.client.delete(f"/todos/{self.todo.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())
