from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    # User urls
    path('user/', views.GenericUser.as_view(), name=views.GenericUser.name),
    path('user/check/', views.CheckUserRegisterEmail.as_view(), name=views.CheckUserRegisterEmail.name),
    path('user/login/', views.LoginUser.as_view(), name=views.LoginUser.name),
    path('user/password/', views.UserChangePassword.as_view(), name=views.UserChangePassword.name),
    path('user/course/', views.UserCourse.as_view(), name=views.UserCourse.name),
    path('user/course/delete/', views.UserCourseDelete.as_view(), name=views.UserCourseDelete.name),


    # Major urls
    path('major/add/', views.AddMajor.as_view(), name=views.AddMajor.name),
    path('major/list/', views.MajorList.as_view(), name=views.MajorList.name),

    # Course urls
    path('course/', views.GenericCourse.as_view(), name=views.GenericCourse.name),

    # Token test urls
    path('user/test/', views.TokenTest.as_view(), name=views.TokenTest.name),



]
