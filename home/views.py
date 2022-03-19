
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

from home.models import SubjectMaster, UserProfile

from .forms import RegistrationForm


def registerPage(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # user = UserProfile.objects.create_user(email=form.cleaned_data.get('email'),username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            # user.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            auth = authenticate(username)
            
            messages.success(request, 'Account was created for ' + username )
            
                

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
    role = request.user.groups.all()[0].name
    all_subject =  SubjectMaster.objects.all().values_list('id','name')
    print(all_subject)
    print(role)
    if role:
        return render(request, 'home.html', {'role': role, 'all_subject': all_subject})
    return render(request, 'home.html')


@login_required(login_url='/login/')
def attendance(request):
    role = request.user.groups.all()[0].name
    return render(request,'attendance.html', {'role': role})


@login_required(login_url='/login/')
def more(request):
    role = request.user.groups.all()[0].name
    return render(request,'more.html', {'role': role})