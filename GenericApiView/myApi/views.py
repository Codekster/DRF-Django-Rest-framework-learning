from django.shortcuts import render
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin
from .serializers import EmployeesSerializer
from rest_framework.generics import GenericAPIView
from .models import Employees


# ===============================================
# EMPLOYEES LIST VIEW - Collection Operations
# ===============================================
# URL: /Employees/
# Purpose: Handle operations on multiple employees (list all, create new)
# HTTP Methods: GET (list all), POST (create new)
class EmployeesList(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset = Employees.objects.all()
    serializer_class= EmployeesSerializer

    def get(self, request, *args, **kwargs):
        """
        GET /Employees/
        Returns a list of all employees in the database
        Uses ListModelMixin.list() method
        """
        return self.list(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        """
        POST /Employees/
        Creates a new employee with data from request body
        Uses CreateModelMixin.create() method
        Expected JSON: {"name": "John", "age": 30, "salary": 50000}
        """
        return self.create(request,*args,**kwargs)

    
# ===============================================
# EMPLOYEE MANIPULATION VIEW - Individual Operations  
# ===============================================
# URL: /Employees/{id}/
# Purpose: Handle operations on a single employee (get, update, delete)
# HTTP Methods: GET (retrieve), PUT (full update), PATCH (partial update), DELETE (remove)
class EmployeesManipulation(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset=Employees.objects.all()
    serializer_class=EmployeesSerializer

    def get(self,request, *args,**kwargs):
        """
        GET /Employees/{id}/
        Retrieves a specific employee by their ID
        Uses RetrieveModelMixin.retrieve() method
        Example: GET /Employees/1/ returns employee with ID 1
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        PUT /Employees/{id}/
        Fully updates an existing employee (all fields required)
        Uses UpdateModelMixin.update() method  
        Expected JSON: {"name": "John Updated", "age": 35, "salary": 60000}
        """
        return self.update(request,*args,**kwargs)

    def patch(self, request, *args, **kwargs):
        """
        PATCH /Employees/{id}/
        Partially updates an existing employee (only provided fields)
        Uses UpdateModelMixin.partial_update() method
        Expected JSON: {"salary": 70000} (only updates salary)
        """
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self,request,*args,**kwargs):
        """
        DELETE /Employees/{id}/
        Deletes a specific employee by their ID
        Uses DestroyModelMixin.destroy() method
        Returns 204 No Content on successful deletion
        """
        return self.destroy(request,*args,**kwargs)


# ===============================================
# API ENDPOINTS SUMMARY:
# ===============================================
# GET    /Employees/     -> List all employees
# POST   /Employees/     -> Create new employee
# GET    /Employees/1/   -> Get employee with ID 1  
# PUT    /Employees/1/   -> Update employee with ID 1 (full update)
# PATCH  /Employees/1/   -> Update employee with ID 1 (partial update)
# DELETE /Employees/1/   -> Delete employee with ID 1
# ===============================================
    




