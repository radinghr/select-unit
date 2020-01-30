from django.db import models
from django.contrib.auth.models import AbstractUser


class Major(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=120, default=None, null=True)
    teacher_name = models.CharField(max_length=120, default=None, null=True)
    exam_time = models.CharField(max_length=120, default=None, null=True)
    exam_day = models.CharField(max_length=120, default=None, null=True)
    daily_time = models.CharField(max_length=120, default=None, null=True)
    day = models.CharField(max_length=120, default=None, null=True)
    major = models.ForeignKey(Major, null=True, on_delete=models.SET_NULL)
    semester = models.IntegerField(default=1)
    type = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(AbstractUser):
    student_number = models.CharField(max_length=120, default=None, null=True)
    full_name = models.CharField(max_length=120, default=None, null=True)
    semester = models.IntegerField(default=1)
    major = models.ForeignKey(Major, null=True, on_delete=models.SET_NULL)
    is_normal_user = models.BooleanField(default=0)

    class Meta:
        ordering = ['semester']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super(User, self).save(*args, **kwargs)


class StudentCourse(models.Model):
    course_id = models.IntegerField(default=0, null=False)
    user_id = models.IntegerField(default=0, null=False)
