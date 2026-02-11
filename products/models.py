from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import CustomUser

class Category(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    text=models.TextField(max_length=150)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

