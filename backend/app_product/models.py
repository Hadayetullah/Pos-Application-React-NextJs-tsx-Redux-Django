from django.db import models

import uuid

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_title = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.category_title
    


class Variant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant_title = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variant_title
    


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_title = models.CharField(max_length=255, unique=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/product', null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, related_name='variants', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_title
    
    def low_stock(self):
        if self.quantity < 5:
            return f'The {self.product_title} quantity is {self.quantity}'
        else:
            return ''




