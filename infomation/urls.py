"""infomation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from index import views
urlpatterns = [
    path('', views.login_view, name='home'),
    path("register_view/", views.register_view, name='register_view'),
    path("admin/", admin.site.urls),
    path("login/", views.login, name='login'),
    path("register/", views.register, name='register'),
    path("main/", views.main_view, name='main'),
    path("patientInHospital/", views.patientInHospital_view, name='patientInHospital'),
    path("patientOutHospital/", views.patientOutHospital_view, name='patientOutHospital'),
    path("in/", views.in_view, name='in'),
    path("out/", views.out_view, name='out'),

]
