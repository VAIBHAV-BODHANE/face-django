# Generated by Django 4.0.3 on 2022-03-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_subjectmaster_teachersubjects_lecturescheduler'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='home/student/images'),
        ),
    ]