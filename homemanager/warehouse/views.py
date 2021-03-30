
from django.views.generic import ListView, TemplateView, DeleteView, View, CreateView
from django.views.generic.detail import DetailView
from django.contrib import messages

from django.core import serializers
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, CategoryForm, HomeForm
from accounts.models import Client
from .models import Home, Product, Category, HomeInvitation
from .utils import OwnershipMixin

import json
# Create your views here.

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'warehouse/home.html'
    def get_queryset(self):
        return Home.objects.filter(client=self.request.user.client)
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        home_form = HomeForm()
        context['home_form'] = home_form
        home_invitations = HomeInvitation.objects.filter(
            invite_to = self.request.user.client
        )
        context['invitations'] = home_invitations
        return context


class CreateHomeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = HomeForm(data = request.POST)
        if form.is_valid():
            obj = form.save(commit=True)
            obj.client.add(self.request.user.client.pk)
            obj.save()
            messages.info(self.request, "Home added")
            return redirect("warehouse:home")
            

class UpdateHomeView(OwnershipMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        home_instance = Home.objects.get(pk=kwargs['pk'])
        form = HomeForm(data = request.POST, instance=home_instance)
        if form.is_valid():
            form.save()
            return redirect('warehouse:home')


class LeaveHomeView(LoginRequiredMixin, OwnershipMixin, View):
    def get(self, *args, **kwargs):
        home = Home.objects.get(pk=kwargs['pk'])
        client = User.objects.get(pk=kwargs['userpk']).client
        if self.request.user.client.pk == client.pk:
            home.client.remove(client)
            messages.info(self.request, "DONE...")
        else:
            messages.info(self.request, "YOU ARE BAD")
        return redirect('warehouse:home')


class DeleteHomeView(LoginRequiredMixin, OwnershipMixin, DeleteView):
    model = Home
    template_name = "warehouse/confirm_home_delete.html"
    success_url = reverse_lazy('warehouse:home')
  

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
        context['invites'] = home_instance.pending_invites()
        return context

    def post(self, request, *args, **kwargs):
        if 'category_add' in request.POST:
            category_form = CategoryForm(client = self.request.user.client, 
                                         data=request.POST or None)
            if category_form.is_valid():
                category_form.save()
            
        if 'product_add' in request.POST:
            home_instance = Home.objects.get(pk=kwargs['pk'])
            product_form = ProductForm(home_instance=home_instance, data=request.POST)
            if product_form.is_valid():
                product_form.save()
            else:
                messages.error(self.request, 'cos nie tak')

        messages.info(self.request, 'messages working')
        return redirect('warehouse:home_detail', self.request.user.pk)


class UpdateProductView(LoginRequiredMixin, OwnershipMixin, View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        form = ProductForm(home_instance=product.category.home, 
                           data=request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.info(self.request, "Product updated")
        else:
            print(form.errors)
            messages.info(self.request, "Form incorrect")
        return HttpResponseRedirect(product.category.home.get_absolute_url())


class UpdateCategoryView(LoginRequiredMixin, OwnershipMixin, View):
    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs.get('pk'))
        form = CategoryForm(client=self.request.user.client, 
                            data=request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.info(request, "Category updated")
        else:
            print(form.errors)
            messages.info(self.request, "Form incorrect")
        return HttpResponseRedirect(category.home.get_absolute_url())
        

class DeleteProductView(LoginRequiredMixin, OwnershipMixin, DeleteView):
    model = Product
    def get(self, request, *args, **kwargs):
        messages.info(self.request, "product deleted!")
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        home = self.object.category.home
        return home.get_absolute_url()
    

class DeleteCategoryView(LoginRequiredMixin, OwnershipMixin, DeleteView):
    model = Category
    template_name = "warehouse/confirm_category_delete.html"
    def get_success_url(self):
        home = self.object.home
        messages.info(self.request, "Category and all products included \
                      in are now deleted")
        return home.get_absolute_url()
  
#TODO: test
class GetClients(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if kwargs['lastname'] != 'none' and kwargs['firstname'] != 'none':
            clients = Client.objects.filter(
                first_name__contains=kwargs['firstname'],
                last_name__contains=kwargs['lastname']
                )
        elif kwargs['lastname'] != 'none':
            clients = Client.objects.filter(
                last_name__contains=kwargs['lastname']
                )
        elif kwargs['firstname'] != 'none':
            clients = Client.objects.filter(
                first_name__contains=kwargs['firstname'],
                )
        else: 
            clients = {}
        #Remove already invited clients
        home = Home.objects.get(pk=self.request.user.client.pk)
        home_invites = HomeInvitation.objects.filter(home=home)
        print(home_invites)
        new_list = clients.exclude(invited_client__in=home_invites).order_by('first_name')[:50]
        client_list = list(new_list.values())
        # for index, client in enumerate(client_list):
        #     cl = Client.objects.get(pk=client['id'])
        #     if cl.is_invited:
        #         client_list.pop(index)
                
        return JsonResponse(client_list, safe=False)


#TODO: test
class HomeInviteView(LoginRequiredMixin, OwnershipMixin, View):
    def get(self, request, *args, **kwargs):
        home_instance = Home.objects.get(pk=kwargs['pk'])
        if self.request.user.client in home_instance.owners.all():
            invited_client = Client.objects.get(pk=kwargs['clientpk'])
            try:
                HomeInvitation.objects.create(
                    home=home_instance,
                    invite_from=self.request.user.client,
                    invite_to=invited_client
                )
            except:
                messages.info(self.request, "Invite is already pending")
                return redirect('warehouse:home_detail', kwargs['pk'])
            messages.info(self.request, f"You have invited {invited_client} \
                          to home home")

            return redirect('warehouse:home_detail', kwargs['pk'])
        else:
            messages.info(self.request, "You are not owner of this home")
            return redirect('warehouse:home_detail', kwargs['pk'])


#TODO: tests
class AcceptHomeInvitation(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        invitation = HomeInvitation.objects.get(pk=kwargs['invpk'])
        if invitation.invite_to == self.request.user.client:
            invitation.home.client.add(self.request.user.client.pk)
            messages.info(self.request, "Welcome")
            return redirect('warehouse:home_detail', invitation.home.pk)
        else:
            messages.info(self.request, "Wrong request")
            return redirect('warehouse:home')


#TODO: tests
class DeclineHomeInvitation(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        invitation = HomeInvitation.objects.get(pk=kwargs['invpk'])
        if invitation.invite_to == self.request.user.client:
            invitation.delete()
            messages.info(self.request, "Invite declined")
        else:
            messages.info(self.request, "Wrong request")
        return redirect('warehouse:home')
