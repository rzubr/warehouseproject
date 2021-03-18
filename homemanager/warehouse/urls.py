from django.urls import path
from .views import HomeView, HomeDetailsView


app_name = 'warehouse'

urlpatterns = [
    path('homes/', HomeView.as_view(), name='home'),
    path('home/<int:pk>/', HomeDetailsView.as_view(), name='home_detail'),
]
