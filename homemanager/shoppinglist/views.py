from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from warehouse.models import Home
from .models import ListProduct, ShoppingList
from .forms import AddProductForm
from .utils import ShoppingListOwnerMixin
# Create your views here.

class ShoppingListView(LoginRequiredMixin, TemplateView):
    template_name = 'shoppinglist/shopping_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_product_form"] = AddProductForm
        context['home'] = Home.objects.get(pk=kwargs['homepk'])
        context['shopping_list'] = ShoppingList.objects.get(pk=kwargs['listpk'])
        return context
    

class GetLProductsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        home = Home.objects.get(pk = kwargs['homepk'])
        shopping_list = ShoppingList.objects.get(pk=kwargs['listpk'])
        products = ListProduct.objects.filter(shopping_list=shopping_list)
        products_list = list(products.values())
        return JsonResponse(products_list, safe=False)


class AddLProductView(LoginRequiredMixin, View):
    pass


class DeleteLProductView(LoginRequiredMixin, ShoppingListOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        list_product = ListProduct.objects.get(pk=kwargs['lprodpk'])
        product_name = list_product.name
        list_product.delete()
        return JsonResponse({'result':f'Deleted {product_name}'})


# class CompleteLProductView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         pass


class ChangeProductStatusView(LoginRequiredMixin, ShoppingListOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        list_product = ListProduct.objects.get(pk=kwargs['lprodpk'])

        if list_product.status == 'R':
            list_product.status = 'C'
        else:
            list_product.status = 'R'
        list_product.save()
        return JsonResponse({'result': 'Done'})


class ResetLProductStatus(LoginRequiredMixin,View):
    pass


