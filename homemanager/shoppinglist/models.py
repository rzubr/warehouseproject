from django.db import models
from warehouse.models import Home, Product
# Create your models here.

STATUS_CHOICES = (
    ('R', 'Requested'),
    ('D', 'Done')
)


class ShoppingList(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=64, default='R')

    def __str__(self):
        return f'List for {self.home}, created {self.created_date}'


class ListProduct(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    status = models.CharField(choices=STATUS_CHOICES, max_length=64, default='R')

    def __str__(self):
        return f'{self.name} product for home: {self.shopping_list.home}'
    

