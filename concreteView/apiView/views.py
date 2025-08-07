from django.shortcuts import render
from rest_framework import generics
from .serializers import EmployeesSerializer
from .models import Employees

class listCreateEmployees(generics.ListCreateAPIView):
    queryset= Employees.objects.all()
    serializer_class=EmployeesSerializer


class RetrieveUpdateDestroyEmployees(generics.RetrieveUpdateDestroyAPIView):
    queryset= Employees.objects.all()
    serializer_class=EmployeesSerializer


