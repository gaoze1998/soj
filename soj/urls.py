"""soj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from soj.oj import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('contests/', views.ContestList.as_view()),
    path('contest/<int:pk>/problems', views.ContestProblemsList.as_view()),
    path('problem/<int:contest_id>/<int:pk>/', views.ProblemDetail.as_view()),
    path('submit/<int:contest_id>/<int:problem_id>/', views.Submit.as_view()),
]
