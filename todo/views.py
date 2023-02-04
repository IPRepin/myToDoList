from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')


def singup_user(request):
    if request.method == 'GET':
        return render(request, 'singup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'singup_user.html', {'form': UserCreationForm(), 'error': 'Имя пользователя занято'})
        else:
            return render(request, 'singup_user.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'} )

def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form': AuthenticationForm(), 'error': 'Логин или пароль не найдены'})
        else:
            login(request, user)
            return redirect('current_todos')

@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def create_todos(request):
    if request.method == 'GET':
        return render(request, 'create.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'create.html', {'form': TodoForm(), 'error':'Неверные данные'})

@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'current_todos.html', {'todos':todos})

@login_required
def complited_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'complited_todos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'viewtodo.html', {'todo': todo, 'form': form, 'error': 'Неверная информация'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('current_todos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')
