
import imp
import profile
import re
import django
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

from home.models import SubjectMaster, UserProfile, TeacherSubjects, LectureScheduler, LectureAttendance
from myapp.settings import TIME_ZONE

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
    print(role)
    all_subject = None
    all_teacher = None
    your_subject = None
    curr_lecture = None
    upcoming_lecture = None
    profile_pic = True

    if role == 'Student':
        if (request.user.profile_pic == None) or (request.user.profile_pic == ''):
            profile_pic=False
        else:
            curr = datetime.now()
            date_end = (datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(days=1)) + timedelta(hours=3)
            curr_lecture = LectureScheduler.objects.filter(start_time__lte=curr, end_time__gte=curr).values_list('teacher__teacher__username', 'subject__name', 'start_time', 'end_time', 'id')
            upcoming_lecture = LectureScheduler.objects.filter(start_time__gte=curr, end_time__lte=date_end).values_list('teacher__teacher__username', 'subject__name', 'start_time', 'end_time')
            if len(curr_lecture) == 0:
                curr_lecture = 0
            else:
                curr_lecture = curr_lecture[0]

            if len(upcoming_lecture) == 0:
                upcoming_lecture = 0


    if role == 'Admin':
        all_subject =  SubjectMaster.objects.all().values_list('id','name')
        all_teacher = UserProfile.objects.filter(is_staff=True)
        for i in all_teacher:
            if 'Teacher' in i.groups.all().values_list('name', flat=True):
                pass

            else:
                all_teacher = all_teacher.exclude(id=i.id)
    if role == 'Teacher':
        your_subject = TeacherSubjects.objects.filter(teacher__id=request.user.id).values_list('subject__id', 'subject__name')
    if role:
        return render(request, 'home.html', {'role': role, 'user': (request.user.username).title(), 'user_id': request.user.id, 'all_subject': all_subject, 'all_teacher': all_teacher, 'your_subject': your_subject, 'curr_lecture': curr_lecture, 'upcoming_lecture': upcoming_lecture, 'profile_pic': profile_pic})
    return render(request, 'home.html')


@login_required(login_url='/login/')
def attendance(request):
    role = request.user.groups.all()[0].name
    return render(request,'attendance.html', {'role': role})


@login_required(login_url='/login/')
def more(request):
    role = request.user.groups.all()[0].name
    return render(request,'more.html', {'role': role})


@login_required(login_url='/login/')
def add_teacher_subject(request):
    """Add teacher with thier corressponding subject"""

    if request.POST:
        subject_id = request.POST.get('subject_id')
        teacher_id = request.POST.get('teacher_id')

        sub = SubjectMaster.objects.get(id=subject_id)
        teacher = UserProfile.objects.get(id=teacher_id)
        add_subject = TeacherSubjects(teacher=teacher,subject=sub)
        add_subject.save()
        con=True
    
    return render(request, 'home.html', {'con': con})


@login_required(login_url='/login/')
def schedule_lecture_time(request):
    """Teacher schedule the lecture"""

    if request.POST:
        teacher_id = request.POST.get('teacher_id')
        subject_id = request.POST.get('subject_id')
        fromTime = request.POST.get('fromTime')
        toTime = request.POST.get('toTime')

        print(request.POST)

        sub = SubjectMaster.objects.get(id=subject_id)
        teacher = TeacherSubjects.objects.get(teacher=teacher_id, subject=subject_id)
        schedule_lecture = LectureScheduler(teacher=teacher, subject=sub, start_time=fromTime, end_time=toTime)
        schedule_lecture.save()
        con = True
    
    return render(request, 'home.html', {'con': con})


@login_required(login_url='/login/')
def add_profile_pic(request):
    """Add student profile picture"""

    if request.POST:
        student_id = request.GET.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        print(profile_pic)
        print(request.FILES)
        user = UserProfile.objects.get(id=student_id)
        fs=FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        url = fs.url(filename)
        user.profile_pic=url
        user.save()
        con = True
    
    return render(request, 'home.html', {'con': con})


def findEncodings(images):
    encodeList = []
    
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


@login_required(login_url='/login/')
def student_face_recognition(request):
    """Recoginise the face"""
    lecSche = request.GET.get('lecSche')
    path = 'media'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    # print(u.profile_pic.name == '/media/'+str(myList[0]))

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    # while True:
    success, img = cap.read()
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    name = None
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
# print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
# print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    index = classNames.index(name)
    u = UserProfile.objects.get(profile_pic='/media/'+str(myList[index]))
    res = markAttendance(u,lecSche)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)

    return render(request, 'home.html', {'con':res})


def markAttendance(stu_obj, lec_obj):
    """Mark the attendance"""
    lecture = LectureScheduler.objects.get(id=lec_obj)
    attendance = LectureAttendance(student=stu_obj,lecture_schedule=lecture)
    attendance.save()
    return True

    
    

