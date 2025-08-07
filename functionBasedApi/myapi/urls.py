from django.urls import path
from . import views

urlpatterns=[
    path('notes/',views.notesApi,name='notesApi'),
    path('notes/<int:id>/',views.notesApi, name='notesApiWithId'),
]