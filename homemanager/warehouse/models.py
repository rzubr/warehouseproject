from django.db import models
from accounts.models import Client
from django.urls import reverse
import datetime

# Create your models here.


class Home(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, unique=False)
    owners = models.ManyToManyField(Client, related_name='owners')
    client = models.ManyToManyField(Client)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("warehouse:home_detail", kwargs={"pk": self.pk})

    def pending_invites(self):
        return self.homeinvitation_set.all()
        

class HomeInvitation(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    invite_from = models.ForeignKey(Client, on_delete=models.CASCADE)
    invite_date = models.DateTimeField(auto_now_add=True, editable=False)
    invite_to = models.ForeignKey(Client, on_delete=models.RESTRICT, related_name='invited_client', null=True, blank=True)

    def __str__(self):
        return "Request to access {} from {}, {}".format(self.home, 
            self.invite_from, self.invite_date.strftime("%Y-%m-%d-%H:%M:%S"))

    class Meta:
        unique_together = ('home', 'invite_to')


class Category(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name_plural = 'categories'
        unique_together = ('name', 'home')


class Product(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=16, decimal_places=3, null=True, blank=True)
    new_quantity = models.DecimalField(max_digits=16, decimal_places=3, default=0, null=True)
    unit = models.CharField(max_length=32, blank=False, null=False)
    stock = models.CharField(max_length=64, blank=False, null=False, default='Full')
    max_quantity = models.DecimalField(max_digits=16, decimal_places=3, default=0, null=True)

    def __str__(self):
        return str(self.name + ' stock: ' + self.stock)

    def replenish_stock(self, *args, **kwargs):
        self.quantity = self.new_quantity

    def check_stock_state(self, *args, **kwargs):
        stock_state = self.quantity / self.max_quantity
        if stock_state > 0.98:
            self.stock = 'Full'
        elif stock_state > 0.1:
            self.stock = 'OK'
        elif stock_state > 0.01:
            self.stock = 'Ends'
        else:
            self.stock = 'empty'

    def save(self, *args, **kwargs):
        self.max_quantity = max(self.max_quantity, self.new_quantity)
        self.quantity = self.new_quantity
        self.check_stock_state()
        super(Product, self).save(*args, **kwargs)
    
    class Meta:
        unique_together = ('name', 'category')