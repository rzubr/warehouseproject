from .models import ListProduct, ShoppingList
from django.http import JsonResponse

class ShoppingListOwnerMixin:

    def dispatch(self, request, *args, **kwargs):
        lprod = ListProduct.objects.get(pk=kwargs['lprodpk'])
        requested_list = ShoppingList.objects.get(pk=kwargs['listpk'])

        if lprod.shopping_list == requested_list and \
           request.user.client in lprod.shopping_list.home.client.all():
            return super().dispatch(request, *args, **kwargs)
        else:
            return JsonResponse({'result':'Bad request'})