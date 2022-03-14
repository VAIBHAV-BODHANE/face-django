
import imp
import re
import django
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# import face_recognition
from django.contrib.auth.decorators import login_required
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user )
            
                

            return redirect('login')



    context = {'form' :form}
    return render(request, 'register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username , password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            username = request.POST['username']
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'login.html', {'username': username})
    context ={}
    return render(request, 'login.html', context)


@login_required(login_url='/login/')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def index(request):
    role = request.user.groups.all()
    print(role)
    if role:
        return render(request, 'home.html', {'role': role[0].name})
    return render(request, 'home.html')


@login_required(login_url='/login/')
def attendance(request):
    return render(request,'attendance.html')


@login_required(login_url='/login/')
def more(request):
    return render(request,'more.html')