# Django REST Framework (DRF) - Learning Guide
*Concise & Organized Reference - Lectures 1-14*

## 📊 Progress: 14/35 Videos ✅ (40% Complete)

---

## 📚 Quick Navigation
1. [🔥 Core Concepts](#core-concepts)
2. [⚡ Function-Based Views](#function-based-views)
3. [🏗️ Class-Based Views](#class-based-views)
4. [🎯 GenericAPIView & Mixins](#genericapiview--mixins)
5. [🔄 CRUD Operations](#crud-operations)
6. [✅ Validation](#validation)
7. [🚀 Quick Reference](#quick-reference)

---

## 🔥 Core Concepts

### 🌟 API Fundamentals
**API** = Waiter between client and server  
**REST** = Set of rules for building APIs  
**DRF** = Django toolkit for building APIs

**HTTP Methods:**
- `GET` → Read data
- `POST` → Create data  
- `PUT` → Update data
- `DELETE` → Remove data

### 🔧 Setup & Installation
```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Add this
    'myapi',          # Your app
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
```

### 📊 Models
```python
# models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Notes(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### 🔧 Serializers
**Purpose:** Convert between Python objects ↔ JSON

```python
# serializers.py
from rest_framework import serializers
from .models import Notes, Student

# ModelSerializer (Recommended)
class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'
        # Alternative options:
        # fields = ['title', 'completed']
        # exclude = ['created_at']

# Basic Serializer (Manual control)
class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    roll = serializers.IntegerField()
    city = serializers.CharField(max_length=100)
    
    def create(self, validated_data):
        return Student.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.roll = validated_data.get('roll', instance.roll)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance
```

---

## ⚡ Function-Based Views

```python
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Notes
from .serializers import NotesSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def notes_api(request, id=None):
    """Complete CRUD API using function-based view"""
    
    # GET - Read operations
    if request.method == 'GET':
        if id:
            try:
                note = Notes.objects.get(id=id)
                serializer = NotesSerializer(note)
                return Response({
                    'success': True,
                    'data': serializer.data
                })
            except Notes.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Note not found'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            notes = Notes.objects.all()
            serializer = NotesSerializer(notes, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'count': len(serializer.data)
            })
    
    # POST - Create operation
    elif request.method == 'POST':
        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Note created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # PUT - Update operation
    elif request.method == 'PUT':
        pk = request.data.get('id')
        if not pk:
            return Response({
                'success': False,
                'message': 'ID required for update'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            note = Notes.objects.get(id=pk)
            serializer = NotesSerializer(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'data': serializer.data,
                    'message': 'Note updated successfully'
                })
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Notes.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Note not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    # DELETE - Delete operation
    elif request.method == 'DELETE':
        if not id:
            return Response({
                'success': False,
                'message': 'ID required for deletion'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            note = Notes.objects.get(id=id)
            note.delete()
            return Response({
                'success': True,
                'message': 'Note deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Notes.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Note not found'
            }, status=status.HTTP_404_NOT_FOUND)
```

**URLs:**
```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.notes_api, name='notes-list'),
    path('notes/<int:id>/', views.notes_api, name='notes-detail'),
]

# Main project urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapi.urls')),
]
```

---

## 🏗️ Class-Based Views

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notes
from .serializers import NotesSerializer

class NotesAPIView(APIView):
    """Complete CRUD API using class-based view"""
    
    def get(self, request, pk=None):
        """Handle GET requests"""
        if pk:
            try:
                note = Notes.objects.get(id=pk)
                serializer = NotesSerializer(note)
                return Response({
                    'success': True,
                    'data': serializer.data
                })
            except Notes.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Note not found'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            notes = Notes.objects.all()
            serializer = NotesSerializer(notes, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'count': len(serializer.data)
            })
    
    def post(self, request):
        """Handle POST requests"""
        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Note created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """Handle PUT requests"""
        try:
            note = Notes.objects.get(id=pk)
            serializer = NotesSerializer(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'data': serializer.data,
                    'message': 'Note updated successfully'
                })
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Notes.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Note not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        """Handle DELETE requests"""
        try:
            note = Notes.objects.get(id=pk)
            note.delete()
            return Response({
                'success': True,
                'message': 'Note deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Notes.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Note not found'
            }, status=status.HTTP_404_NOT_FOUND)
```

**URLs:**
```python
# urls.py
from django.urls import path
from .views import NotesAPIView

urlpatterns = [
    path('notes/', NotesAPIView.as_view(), name='notes-list'),
    path('notes/<int:pk>/', NotesAPIView.as_view(), name='notes-detail'),
]
```

---

## 🎯 GenericAPIView & Mixins (Lecture 14)

### 🌟 Why GenericAPIView + Mixins?
**GenericAPIView** provides the foundation (queryset, serializer, lookup)  
**Mixins** provide the CRUD operations (list, create, retrieve, update, destroy)  
**Together** = Powerful APIs with minimal code!

### 🔧 Complete Implementation
```python
# views.py
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,      # GET all objects
    CreateModelMixin,    # POST new object  
    RetrieveModelMixin,  # GET single object
    UpdateModelMixin,    # PUT/PATCH object
    DestroyModelMixin    # DELETE object
)
from rest_framework.response import Response
from .models import Notes
from .serializers import NotesSerializer

class NotesAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, 
                   UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    Complete CRUD API using GenericAPIView + Mixins
    Less code, more power!
    """
    # GenericAPIView attributes
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    lookup_field = 'pk'
    
    # Optional: Override queryset for filtering
    def get_queryset(self):
        """Filter by authenticated user"""
        return Notes.objects.filter(owner=self.request.user)
    
    # HTTP method handlers - connect to mixins
    def get(self, request, *args, **kwargs):
        """Handle GET requests"""
        if 'pk' in kwargs:
            # GET single object: /api/notes/1/
            return self.retrieve(request, *args, **kwargs)
        else:
            # GET all objects: /api/notes/
            return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests: /api/notes/"""
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """Handle PUT requests: /api/notes/1/"""
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests: /api/notes/1/"""
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """Handle DELETE requests: /api/notes/1/"""
        return self.destroy(request, *args, **kwargs)
```

### 🔧 URLs Configuration
```python
# urls.py
from django.urls import path
from .views import NotesAPIView

urlpatterns = [
    # Collection endpoint (GET all, POST new)
    path('notes/', NotesAPIView.as_view(), name='notes-list'),
    
    # Detail endpoint (GET/PUT/PATCH/DELETE single)
    path('notes/<int:pk>/', NotesAPIView.as_view(), name='notes-detail'),
]
```

### 🧩 What Each Mixin Provides

| Mixin | Method | HTTP | URL | Purpose |
|-------|--------|------|-----|---------|
| **ListModelMixin** | `list()` | GET | `/notes/` | Get all objects |
| **CreateModelMixin** | `create()` | POST | `/notes/` | Create new object |
| **RetrieveModelMixin** | `retrieve()` | GET | `/notes/1/` | Get single object |
| **UpdateModelMixin** | `update()` | PUT | `/notes/1/` | Full update |
| **UpdateModelMixin** | `partial_update()` | PATCH | `/notes/1/` | Partial update |
| **DestroyModelMixin** | `destroy()` | DELETE | `/notes/1/` | Delete object |

### 🎯 Key GenericAPIView Attributes
```python
class NotesAPIView(GenericAPIView):
    # Required attributes
    queryset = Notes.objects.all()           # Data source
    serializer_class = NotesSerializer       # How to serialize
    
    # Optional attributes  
    lookup_field = 'pk'                      # Lookup field (default: pk)
    lookup_url_kwarg = 'pk'                  # URL parameter name
    pagination_class = PageNumberPagination  # Pagination
    filter_backends = [SearchFilter]         # Filtering
    search_fields = ['title', 'content']     # Search fields
```

### 🔧 Key GenericAPIView Methods
```python
# Override these methods for custom behavior
def get_queryset(self):
    """Return filtered queryset"""
    return Notes.objects.filter(owner=self.request.user)

def get_object(self):
    """Return single object with custom logic"""
    obj = super().get_object()
    # Add permission checks here
    return obj

def get_serializer_class(self):
    """Return different serializers for different actions"""
    if self.request.method == 'POST':
        return NotesCreateSerializer
    return NotesSerializer

def get_serializer_context(self):
    """Add extra context to serializer"""
    context = super().get_serializer_context()
    context['user'] = self.request.user
    return context
```

### ✅ Benefits of GenericAPIView + Mixins
1. **Less Code** - No need to write CRUD logic yourself
2. **Consistent** - Standard DRF responses and error handling  
3. **Flexible** - Override methods for custom behavior
4. **Powerful** - Built-in pagination, filtering, permissions
5. **Reusable** - Same pattern works for any model

### 🎯 API Endpoints Created
```bash
# Test your API endpoints
GET    /api/notes/         # List all notes
POST   /api/notes/         # Create new note
GET    /api/notes/1/       # Get note with ID 1
PUT    /api/notes/1/       # Update note with ID 1 (full)
PATCH  /api/notes/1/       # Update note with ID 1 (partial)
DELETE /api/notes/1/       # Delete note with ID 1
```

### 🚀 Example Requests
```bash
# Create note
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "content": "Note content"}'

# Get all notes  
curl -X GET http://localhost:8000/api/notes/

# Update note (partial)
curl -X PATCH http://localhost:8000/api/notes/1/ \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete note
curl -X DELETE http://localhost:8000/api/notes/1/
```

---

## 🔄 CRUD Operations

### 📊 Complete Working Example
Here's everything you need for a complete CRUD API:

**1. Models (models.py):**
```python
from django.db import models

class Notes(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
```

**2. Serializers (serializers.py):**
```python
from rest_framework import serializers
from .models import Notes

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
```

**3. Views (views.py) - Choose one approach:**

**Option A: Function-Based (Simple):**
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def notes_crud(request, pk=None):
    if request.method == 'GET':
        if pk:
            note = Notes.objects.get(id=pk)
            serializer = NotesSerializer(note)
        else:
            notes = Notes.objects.all()
            serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        note = Notes.objects.get(id=pk)
        serializer = NotesSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        note = Notes.objects.get(id=pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**Option B: Mixins (Recommended):**
```python
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

class NotesAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, 
                   UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

**4. URLs (urls.py):**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.notes_crud, name='notes-list'),
    path('notes/<int:pk>/', views.notes_crud, name='notes-detail'),
    
    # Alternative for class-based:
    # path('notes/', views.NotesAPIView.as_view()),
    # path('notes/<int:pk>/', views.NotesAPIView.as_view()),
]
```

**5. Test Your API:**
```bash
# Get all notes
curl -X GET http://localhost:8000/api/notes/

# Create note
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "content": "Note content"}'

# Get single note
curl -X GET http://localhost:8000/api/notes/1/

# Update note
curl -X PUT http://localhost:8000/api/notes/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Note", "completed": true}'

# Delete note
curl -X DELETE http://localhost:8000/api/notes/1/
```

### 🔄 CRUD Operations Summary
- **Create:** `POST /api/notes/` - Send JSON data
- **Read:** `GET /api/notes/` (all) or `GET /api/notes/1/` (single)
- **Update:** `PUT /api/notes/1/` - Send complete JSON data
- **Delete:** `DELETE /api/notes/1/` - No data needed

---

## ✅ Validation

### 🔧 Field-Level Validation
```python
# serializers.py
from rest_framework import serializers
import re

class NotesSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        """Validate title field"""
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters")
        if len(value) > 100:
            raise serializers.ValidationError("Title too long")
        return value
    
    def validate_content(self, value):
        """Validate content field"""
        if 'spam' in value.lower():
            raise serializers.ValidationError("Content contains prohibited words")
        return value
    
    class Meta:
        model = Notes
        fields = '__all__'
```

### 🔧 Object-Level Validation
```python
class EventSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """Validate entire object"""
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(
                    "Start date must be before end date"
                )
        
        if data.get('discount', 0) > 100:
            raise serializers.ValidationError(
                "Discount cannot exceed 100%"
            )
        
        return data
    
    class Meta:
        model = Event
        fields = '__all__'
```

### 🔧 Custom Validators
```python
# validators.py
import re
from rest_framework import serializers

def validate_phone(value):
    """Reusable phone validator"""
    pattern = r'^\+?1?\d{9,15}$'
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )

def validate_strong_password(value):
    """Strong password validator"""
    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', value):
        raise serializers.ValidationError("Password must contain at least one uppercase letter")
    if not re.search(r'[0-9]', value):
        raise serializers.ValidationError("Password must contain at least one number")

# Using custom validators
class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[validate_phone])
    password = serializers.CharField(validators=[validate_strong_password], write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']
```

### 🔧 Built-in Validators
```python
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[MinLengthValidator(3), MaxLengthValidator(20)]
    )
    email = serializers.EmailField(validators=[EmailValidator()])
    age = serializers.IntegerField(min_value=18, max_value=100)
    
    class Meta:
        model = Profile
        fields = '__all__'
```

---

## 🚀 Quick Reference

### 📋 HTTP Status Codes
```
200 OK - Success
201 Created - Created successfully
400 Bad Request - Validation error
404 Not Found - Resource not found
500 Internal Server Error - Server error
```

### 🔧 Common Imports
```python
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
```

### 🛠️ Testing Commands
```bash
# Setup
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Test with curl
curl -X GET http://localhost:8000/api/notes/
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Note"}'
```

### 🎯 Best Practices
1. Use `ModelSerializer` for simple cases
2. Use `GenericAPIView` + mixins for reusability
3. Always validate data
4. Use proper HTTP status codes
5. Handle errors gracefully

---

*📚 Based on: deserializer/, functionBasedApi/, update_and_delete/ projects*
*🎯 Current Progress: Lecture 14/35 - GenericAPIView & Mixins*
*📅 Last Updated: July 29, 2025*
