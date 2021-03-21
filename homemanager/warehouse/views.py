
from django.views.generic import ListView, TemplateView, DeleteView, View
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, CategoryForm
from .models import Home, Product, Category
from .utils import ProductOwnerMixin, CategoryOwnerMixin

# Create your views here.

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'warehouse/home.html'

    def get_queryset(self):
        return Home.objects.filter(client=self.request.user.client)


class HomeDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'warehouse/home_detail.html'
    product_form = ProductForm
    def get_context_data(self, *args, **kwargs):
        context = super(HomeDetailsView, self).get_context_data(*args, **kwargs)
        #get client home instance
        home_instance = Home.objects.get(pk=kwargs['pk'])
        context['home'] = home_instance
        context['categories'] = Category.objects.filter(home=home_instance)
        #get category form
        category_form = CategoryForm(client=self.request.user.client)
        context['category_form'] = category_form
        #get product form
        product_form = ProductForm(home_instance=home_instance)
        context['product_form'] = product_form
        return context

    def post(self, request, *args, **kwargs):
        
        if 'category_add' in request.POST:
            category_form = CategoryForm(client = self.request.user.client, data=request.POST or None)
            if category_form.is_valid():
                category_form.save()
            
        if 'product_add' in request.POST:
            home_instance = Home.objects.get(pk=kwargs['pk'])
            product_form = ProductForm(data=request.POST)
            if product_form.is_valid():
                product_form.save()
            else:
                messages.error(self.request, 'cos nie tak')

        messages.info(self.request, 'messages working')
        return redirect('warehouse:home_detail', self.request.user.pk)


class UpdateProductView(ProductOwnerMixin, LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        form = ProductForm(home_instance=product.category.home, 
                           data=request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.info(self.request, "Product updated")
        else:
            messages.info(self.request, "Form incorrect")
        return HttpResponseRedirect(product.category.home.get_absolute_url())


class UpdateCategoryView(CategoryOwnerMixin, LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs.get('pk'))
        form = CategoryForm(client=self.request.user.client, 
                            data=request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.info(request, "Category updated")
        else:
            messages.info(self.request, "Form incorrect")
        return HttpResponseRedirect(category.home.get_absolute_url())
        

class DeleteProductView(ProductOwnerMixin, LoginRequiredMixin, DeleteView):
    model = Product

    def get(self, request, *args, **kwargs):
        messages.info(self.request, "product deleted!")
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        home = self.object.category.home
        return home.get_absolute_url()
    

class DeleteCategoryView(CategoryOwnerMixin, LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "warehouse/confirm_category_delete.html"
    
    def get_success_url(self):
        home = self.object.home
        messages.info(self.request, "Category and all products included in are now deleted")
        return home.get_absolute_url()
  



