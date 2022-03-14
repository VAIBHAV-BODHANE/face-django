from django.urls import path
from home import views

urlpatterns = [
    path('', views.registerPage, name = 'register'),
    path('login/', views.loginPage, name = 'login'),
    path('home/', views.index, name = 'home'),
    path('attendance/', views.attendance, name = 'attendance'),
    path('more/', views.more, name = 'more'),
    path('logout/', views.logoutUser, name = 'logout'),

]