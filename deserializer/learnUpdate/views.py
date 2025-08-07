from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
import io
from .models import Employees
from .serializers import EmployeesSerializer
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def EmployeesWork(request):
    if request.method == 'PUT':
        try:
            stream = io.BytesIO(request.body)
            updateData = JSONParser().parse(stream)

            id = updateData.get('id')
            if not id:
                return JsonResponse({'msg': 'ID is required for update'}, status=400)

            try:
                instance = Employees.objects.get(id=id)
            except Employees.DoesNotExist:
                return JsonResponse({'msg': f'Employee with id {id} not found'}, status=404)
        #------------------------------------------------------------------------------------------
            #here partial=true alllows us to update only the fields provided in the request
            # if we want to update all fields then we can remove partial=true
            # and use EmployeesSerializer(instance, updateData) instead
            # this will require all fields to be present in the request data
        #------------------------------------------------------------------------------------------

            emp = EmployeesSerializer(instance, updateData, partial=True)
            
            if emp.is_valid():
                emp.save()
                return JsonResponse({'msg': 'Data Updated Successfully'}, status=200)
            else:
                return JsonResponse({'msg': 'Update unsuccessful', 'errors': emp.errors}, status=400)

        except Exception as e:
            return JsonResponse({'msg': 'Something went wrong', 'error': str(e)}, status=500)

    return HttpResponse('Method Not Allowed', status=405)
        
        

    
        

    
    

