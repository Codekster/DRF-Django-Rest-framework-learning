from django.urls import path
from . import views

urlpatterns=[
    path('',views.EmployeesList.as_view(),name='GetEmployees'),
    path('<int:pk>/', views.EmployeesManipulation.as_view(), name='ManipulationEmployees')
]