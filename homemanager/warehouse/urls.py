from django.urls import path
from .views import (HomeView, HomeDetailsView, DeleteProductView, 
    DeleteCategoryView, UpdateProductView, UpdateCategoryView, CreateHomeView,
    UpdateHomeView, DeleteHomeView, LeaveHomeView, HomeInviteView, GetClients,
    AcceptHomeInvitation, DeclineHomeInvitation)


app_name = 'warehouse'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/<int:pk>/', HomeDetailsView.as_view(), name='home_detail'),
    path('create_home', CreateHomeView.as_view(), name='create_home'),
    path('update_home/<int:pk>/', UpdateHomeView.as_view(), name='update_home'),
    path('delete_home/<int:pk>/', DeleteHomeView.as_view(), name="delete_home"),
    path('leave_home/<int:pk>/<int:userpk>/', LeaveHomeView.as_view(), name="leave_home"),
    path('delete_category/<int:pk>/', DeleteCategoryView.as_view(), name='delete_category'),
    path('delete_product/<int:pk>/', DeleteProductView.as_view(), name='delete_product'),
    path('update_product/<int:pk>/', UpdateProductView.as_view(), name='update_product'),
    path('update_category/<int:pk>/', UpdateCategoryView.as_view(), name='update_category'),

    path('get_clients/', GetClients.as_view(), name='get_clients'),
    path('get_clients/<slug:firstname>/<slug:lastname>', GetClients.as_view(), name='get_clients'),
    path('home_invite/<int:clientpk>/<int:pk>', HomeInviteView.as_view(), 
        name='home_invite'),
    path('accept_invitation/<int:invpk>', AcceptHomeInvitation.as_view(), name='accept_inv'),
    path('decline_invitation/<int:invpk>', DeclineHomeInvitation.as_view(), name='decline_inv'),
]
