from django.contrib import admin

from .models import Category, Variant, Product


# Register your models here.
admin.site.register(Category)
admin.site.register(Variant)
admin.site.register(Product)
