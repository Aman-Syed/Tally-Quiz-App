"""Quizzery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from QuizApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('login/home/', views.home, name='login/home'),
    path('hometaker/', views.hometaker, name='hometaker'),
    path('upcomingtaker/', views.upcomingtaker, name='upcomingtaker'),
    path('oldquizzes/', views.oldquizzes, name="oldquizzes"),
    path('form/', views.form, name="form"),
    path('upcoming/', views.upcoming, name="upcoming"),
    path('login/register/', views.register, name="register"),
    path('form/creatingquestions/',views.creatingquestions, name="creatingquestions"),
    path('form/creatingquestions/gotoquiz/', views.gotoquiz, name="gotoquiz"),
    path('hometaker/quiz/', views.quiz, name="quiz"),
    path('index/', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('changeend/', views.changeend, name="changeend"),
    # path('userdashboard/', views.userdashboard, name="dashboard"),
    # path('form/creatingquestions/gotoquiz/result', views.result, name="gotoquiz"),


]
