from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Notes
from .serializers import NotesSerializer
from rest_framework import status

@api_view(['GET','POST','PUT','DELETE'])
def notesApi(request,id=None):
    if request.method=='GET':
        pk=request.query_params.get('id',id)
         # or you can use pk=id
        try:
            if pk is not None:
                note=Notes.objects.get(id=pk)
                serializer=NotesSerializer(note)
                return Response({'data':serializer.data, 'msg':'Note retrieved'},status=200)
        except Notes.DoesNotExist:
            return Response({'msg':'Note not found'},status=status.HTTP_404_NOT_FOUND)
        notes=Notes.objects.all()
        serializer=NotesSerializer(notes,many=True)
        return Response({'data':serializer.data,'msg':'All notes retrieved'},status=status.HTTP_200_OK)
    
    if request.method=='POST':
        
        myData=request.data
        serializer=NotesSerializer(data=myData)
    
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data is inserted successfully'})
        else:
            return Response({'error':serializer.errors,'msg':'Data insertion unsuccessfull'},status=status.HTTP_400_BAD_REQUEST)
        

    if request.method=='PUT':
        pk=request.data.get('id',None)

        if pk is not None:
            try:
                note=Notes.objects.get(id=pk)
                serializer=NotesSerializer(note, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Note updated succesfully'},status=status.HTTP_202_ACCEPTED)
                return Response({'error':serializer.errors,'msg':'Note update unsuccessfull'},status=status.HTTP_400_BAD_REQUEST)

            except Notes.DoesNotExist:
                return Response({'msg':'Note not found'},status=status.HTTP_404_NOT_FOUND)
        return Response({'msg':'ID is required for update operation'},status=status.HTTP_400_BAD_REQUEST)

    if request.method=='DELETE':
        pk=request.query_params.get('id',id)
        if pk is not None:
            try:
                note=Notes.objects.get(id=pk)
                note.delete()
                return Response({'msg':'Note deleted successfully'},status=status.HTTP_204_NO_CONTENT)
            except Notes.DoesNotExist:
                return Response({'msg':'Note not found'},status=status.HTTP_404_NOT_FOUND)
        return Response({'msg':'ID is required for deelete operation'},status=status.HTTP_400_BAD_REQUEST)
        
      

