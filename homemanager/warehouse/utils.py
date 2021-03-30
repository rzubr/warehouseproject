from .models import Product, Category, Home
from django.http import HttpResponseRedirect
from django.contrib import messages
import re


class OwnershipMixin:

    def dispatch(self, request, *args, **kwargs):
        product_regexp = re.compile(r'product')
        home_regexp = re.compile(r'home')
        # Regexp is used to recognize model which is included in request by url name 
        if product_regexp.search(str(self.request)):
            home = Product.objects.get(pk=kwargs.get('pk')).category.home
        elif home_regexp.search(str(self.request)):
            home = Home.objects.get(pk=kwargs.get('pk'))
        else:
            home = Category.objects.get(pk=kwargs.get('pk')).home

        client_homes = self.request.user.client.home_set.all()
        if home in client_homes:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.info(self.request, "ITS NOT YOUR PROPERTY")
            return HttpResponseRedirect(home.get_absolute_url())


        