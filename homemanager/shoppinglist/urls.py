from django.urls import path

from .views import ShoppingListView, GetLProductsView, DeleteLProductView, ChangeProductStatusView

app_name = 'shopping_list'

urlpatterns = [
     path("<int:homepk>/<int:listpk>", 
          ShoppingListView.as_view(), name="shopping_list"),
     path("<int:homepk>/<int:listpk>/get_products", GetLProductsView.as_view(), 
          name="get_products"),
     path("delete_list_product/<int:lprodpk>/<int:listpk>", 
          DeleteLProductView.as_view(), 
          name="delete_lproduct"),
     path("change_product_status/<int:lprodpk>/<int:listpk>", 
          ChangeProductStatusView.as_view(), 
          name="change_product_status"),

]
