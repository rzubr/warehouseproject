from django.urls import path
from .views import (HomeView, HomeDetailsView, DeleteProductView, 
    DeleteCategoryView, UpdateProductView, UpdateCategoryView)


app_name = 'warehouse'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/<int:pk>/', HomeDetailsView.as_view(), name='home_detail'),
    path('delete_category/<int:pk>/', DeleteCategoryView.as_view(), name='delete_category'),
    path('delete_product/<int:pk>/', DeleteProductView.as_view(), name='delete_product'),
    path('update_product/<int:pk>/', UpdateProductView.as_view(), name='update_product'),
    path('update_category/<int:pk>/', UpdateCategoryView.as_view(), name='update_category'),
]
