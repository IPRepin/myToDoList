from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

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

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def current_todos(request):
    return render(request, 'current_todos.html')
# Create your views here.
