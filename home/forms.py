from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from home.models import UserProfile
from django import forms





class CreateUserForm(UserCreationForm):
	class Meta:
		model = UserProfile
		fields = ['username', 'email', 'password1', 'password2']