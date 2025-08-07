from django.urls import path
from . import views

urlpatterns=[
    path('', views.EmployeesWork,name='employeesWork'),
]
