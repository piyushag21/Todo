from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

from .views import UserView, signup, login_view

app_name = 'users'

urlpatterns = [
    path('todo/', views.createtodo, name='todo'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
    path('profile/',  login_required(UserView.as_view()), name='profile'),
    path('signup/', signup, name='signup'),
    path('delete/<str:pk>/', views.deleteTodo, name="delete"),
    path('updateTodo/<int:pk>/', views.updateTodo, name="updateTodo"),
]