from django.db import models
from django.contrib.auth.models import AbstractUser


class Major(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class User(AbstractUser):
    student_number = models.CharField(max_length=120, default=0)
    full_name = models.CharField(max_length=120, null=True)
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
