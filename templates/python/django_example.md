# Django Project Example

## Project Structure
```
django-project/
├── myproject/
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── products/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   └── tests.py
│   └── users/
├── static/
├── media/
├── templates/
└── requirements.txt
```

## Development Workflow

1. Create Django app
2. Define models
3. Create migrations
4. Implement views/viewsets
5. Configure URLs
6. Create templates/serializers
7. Write tests

## Example Implementation

### Model
```python
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
```

### ViewSet (DRF)
```python
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def my_products(self, request):
        products = Product.objects.filter(created_by=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
```

### Serializer
```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_by_name', 'created_at']
        read_only_fields = ['id', 'created_at']
```

### URLs
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### Test
```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        
    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.99,
            created_by=self.user
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(str(product), 'Test Product')
```