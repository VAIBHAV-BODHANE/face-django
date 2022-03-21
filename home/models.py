from distutils.command.upload import upload
from ssl import create_default_context
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, User, Permission
import re


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, username, password=None):
        """Create a new user profiles"""
        if not email:
            raise ValueError('User must have an email address!')

        email = self.normalize_email(email)
        print(email)
        user = self.model(email=email, username=username)

        user.set_password(password)
        user.save(using=self._db)

        regex = r'\b[A-Za-z0-9._%+-]+@ourorg.in'
        if re.fullmatch(regex,email):
            print('here1')
            g = Group.objects.filter(name='Teacher')
            user.is_staff=True
        else:
            g = Group.objects.filter(name='Student')
        if len(g):
            print(g)
            user.groups.set(g)
        return user

    def create_superuser(self, email, username, password):
        """Create and save a new superuser with given details"""

        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        regex = r'\b[A-Za-z0-9._%+-]+admin@ourorg.in'
        if re.fullmatch(regex,email):
            g = Group.objects.filter(name='Admin')
        else:
            return None
        user.save(using=self._db)
        if len(g):
            user.groups.set(g)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for use in a system"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    profile_pic = models.ImageField(upload_to='home/student/images', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserProfileManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def get_full_name(self):
        """Retrive full name of user"""
        return self.username


    def get_short_name(self):
        """Retrieve short name of user"""
        return self.username


    def __str__(self):
        """Return string representation of our user"""
        return self.email


class SubjectMaster(models.Model):
    """Master table of subjects"""
    name = models.CharField(max_length=225)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the string respresentation of subject master"""
        return self.name


class TeacherSubjects(models.Model):
    """Teacher details with their corresponding subjects"""
    teacher = models.ForeignKey('home.UserProfile', on_delete=models.CASCADE)
    subject = models.ForeignKey('home.SubjectMaster', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the string respresentation of teacher subject"""
        return self.teacher.username    


class LectureScheduler(models.Model):
    """Keep the lecture time table"""
    subject = models.ForeignKey(SubjectMaster, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    teacher = models.ForeignKey(TeacherSubjects, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.teacher.teacher.username + '-' + self.subject.name


class LectureAttendance(models.Model):
    """Student attendance record"""
    lecture_schedule = models.ForeignKey(LectureScheduler, on_delete=models.CASCADE)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_present = models.CharField(max_length=100, choices=( ('P', 'Present'), ('A', 'Absent') ), default='P')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lecture_schedule.subject.name + '-' + self.student.username + '-' + self.is_present
    

    