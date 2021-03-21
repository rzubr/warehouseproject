from .models import Product, Category
from django.http import HttpResponseRedirect
from django.contrib import messages


class ProductOwnerMixin:

    def dispatch(self, request, *args, **kwargs):
        home = Product.objects.get(pk=kwargs.get('pk')).category.home
        client_homes = self.request.user.client.home_set.all()
        if home in client_homes:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.info(self.request, "ITS NOT YOUR PRODUCT")
            return HttpResponseRedirect(home.get_absolute_url())



class CategoryOwnerMixin:
    
    def dispatch(self, request, *args, **kwargs):
        home = Category.objects.get(pk=kwargs.get('pk')).home
        print(home)
        client_homes = self.request.user.client.home_set.all()
        if home in client_homes:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.info(self.request, "ITS NOT YOUR CATEGORY")
            return HttpResponseRedirect(home.get_absolute_url())


        