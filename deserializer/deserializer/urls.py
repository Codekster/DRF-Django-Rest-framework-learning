from django.contrib import admin
from django.urls import path, include
from learn1 import urls



urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/',include('learn1.urls')),
    path('employees/', include('learnUpdate.urls'), name='learnUpdate'),
]
