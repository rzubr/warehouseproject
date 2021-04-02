from django.contrib import admin

# Register your models here.
from .models import ShoppingList, ListProduct

admin.site.register(ShoppingList)
admin.site.register(ListProduct)