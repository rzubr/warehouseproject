from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='Imie')
    last_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='Last name')
    email = models.EmailField(max_length=64, blank=True, null=True)
    is_owner = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.first_name + " " + self.last_name)
    

