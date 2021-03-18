from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ProductForm, CategoryForm

from .models import Home, Product, Category

# Create your views here.

class HomeView(ListView):
    template_name = 'warehouse/home.html'

    def get_queryset(self):
        return Home.objects.filter(client=self.request.user.client)


class HomeDetailsView(TemplateView):
    template_name = 'warehouse/home_detail.html'
    product_form = ProductForm
    

    # def get(self, request, *args, **kwargs):
    #     product_form = self.product_form(None)
    #     return render(request, self.template_name, {'add_product':product_form})

    def get_context_data(self, *args, **kwargs):
        
        context = super(HomeDetailsView, self).get_context_data(*args, **kwargs)
        #get client home instance
        home_instance = Home.objects.get(pk=kwargs['pk'])
        context['home'] = home_instance
        context['categories'] = Category.objects.filter(home=home_instance)

        #get category add form
        category_form = CategoryForm(user=self.request.user)
        context['category_form'] = category_form

        #get product add form
        
        product_form = ProductForm(home_instance)
        context['product_form'] = product_form

        return context


    def post(self, request, *args, **kwargs):
        
        
        if 'category_add' in request.POST:
            category_form = CategoryForm(self.request.user, request.POST or None)
            if category_form.is_valid():
                category_form.save()
            
        if 'product_add' in request.POST:
            home_instance = Home.objects.get(pk=kwargs['pk'])
            product_form = ProductForm(home_instance, request.POST)
            if product_form.is_valid():
                product_form.save()
            else:
                messages.error('cos nie tak')


        if 'product_edit' in request.POST:
            print('product edit')
        messages.info(self.request, 'messages working')
        return redirect('warehouse:home_detail', self.request.user.pk)
        

    
    
  



