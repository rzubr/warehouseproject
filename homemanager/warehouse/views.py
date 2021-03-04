from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User

from .models import Home, Product, Category

# Create your views here.

class HomeView(ListView):
    template_name = 'warehouse/home.html'
    def get_queryset(self):
        return Home.objects.filter(client=self.request.user.client)


class HomeDetailsView(TemplateView):
    template_name = 'warehouse/home_detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(HomeDetailsView, self).get_context_data(*args, **kwargs)
        home_instance = Home.objects.get(pk=kwargs['pk'])
        context['home'] = home_instance
        context['categories'] = Category.objects.filter(home=home_instance)
        for object in context['categories']:
            prods = Product.objects.filter(category=object)
            print(prods)
        print(type(context['categories']))
        return context
    

