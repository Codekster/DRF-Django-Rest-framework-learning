from django.urls import path
from . import views

urlpatterns=[
    #path('',views.createEmployees.as_view(), name='createEmployees'),
    path('',views.listCreateEmployees.as_view(), name='listEmployees'),

    path('<int:pk>/',views.RetrieveUpdateDestroyEmployees.as_view(), name='deleteEmployees')

]