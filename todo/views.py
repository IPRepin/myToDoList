from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

def singup_user(request):
    if request.method == 'GET':
        return render(request, 'singup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
            except IntegrityError:
                return render(request, 'singup_user.html', {'form': UserCreationForm(), 'error': 'Имя пользователя занято'})
        else:
            return render(request, 'singup_user.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'} )


# Create your views here.
