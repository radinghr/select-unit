from django.contrib import admin
from .models import Major, User, Course, StudentCourse
# Register your models here.

admin.site.register(User)
admin.site.register(Major)
admin.site.register(Course)
admin.site.register(StudentCourse)
