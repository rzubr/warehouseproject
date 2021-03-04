# from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import UserCreateForm
# Create your views here.


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('warehouse:home')
    

class MyLogoutView(LogoutView):
    pass



