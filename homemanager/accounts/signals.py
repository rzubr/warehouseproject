from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Client
from django.http import request


def client_profile(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(
            user = instance,
            first_name = instance.username,
            email = instance.email,
            last_name = ' - '
        )
        print('client created'),

post_save.connect(client_profile, sender=User)

