from django.urls import path
## from .views import LoginView
from .views import MyLoginView, UserCreateView

app_name = 'accounts'

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path("register/", UserCreateView.as_view(), name="register")
]
