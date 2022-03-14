from django.contrib import admin
from .models import UserProfile, SubjectMaster, TeacherSubjects, LectureScheduler

admin.site.register(UserProfile)
admin.site.register(SubjectMaster)
admin.site.register(TeacherSubjects)
admin.site.register(LectureScheduler)
# Register your models here.
