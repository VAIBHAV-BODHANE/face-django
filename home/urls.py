from django.urls import path, re_path
from home import views

urlpatterns = [
    path('', views.registerPage, name = 'register'),
    path('login/', views.loginPage, name = 'login'),
    path('home/', views.index, name = 'home'),
    path('attendance/', views.attendance, name = 'attendance'),
    path('more/', views.more, name = 'more'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('add_teacher_subject/', views.add_teacher_subject, name = 'teacher_subject'),
    re_path(r'schedule_lecture_time/?$', views.schedule_lecture_time, name = 'lecture_time'),
    re_path(r'add_profile_pic/?$', views.add_profile_pic, name = 'profile_pic'),
    path('student_face_recognition/', views.student_face_recognition, name='student_face_recognition'),
]