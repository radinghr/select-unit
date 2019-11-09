from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    # User urls
    path('user/register/', views.RegisterUser.as_view(), name=views.RegisterUser.name),
    path('user/login/', views.LoginUser.as_view(), name=views.LoginUser.name),

    # Major urls
    path('major/add/', views.AddMajor.as_view(), name=views.AddMajor.name),
    path('major/list/', views.MajorList.as_view(), name=views.MajorList.name),

    # Token test urls
    path('user/test/', views.TokenTest.as_view(), name=views.TokenTest.name),



]
