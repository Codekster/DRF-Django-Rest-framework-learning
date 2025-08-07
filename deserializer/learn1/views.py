from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .seerializers import StudentSerializer
from rest_framework.renderers import JSONRenderer 
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # This decorator is used to exempt the view from CSRF verification

# Create your views here.

def student_list(req):
    if req.method == 'POST':
        # Handle the POST request
        json_data=req.body # Get the raw JSON data from the request body

        # Create a stream from the JSON data
        stream=io.BytesIO(json_data) 

        # Parse the JSON data into Python data structure
        python_data=JSONParser().parse(stream) 
        # Here you can save the data to the database or process it as needed

        serializer=StudentSerializer(data = python_data) # to De-Serialize the data

        # Validate the data
        if serializer.is_valid():
            serializer.save()
            res={'msg':'Data inserted Successfully'}
            myData=JSONRenderer().render(res)# dictionary to JSON format
            # Return a success response with the serialized data
            return HttpResponse(myData,content_type='application/json')
        else:
            # If validation fails, return the errors
            myData=JSONRenderer().render(serializer.errors)
            return HttpResponse(myData,content_type='application/json')   
    else:
        return JsonResponse({'msg': 'Only POST allowed'}, status=405)
    
   


