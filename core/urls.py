from django.contrib import admin
from django.urls import path
from core import views
from .views import *
from .login import *

urlpatterns = [
    path('users/', users_db_operations.as_view(), name='users_db_operations'),
    path('users/<int:user_id>/', users_db_operations.as_view(), name='user_detail'),
    path('users/<str:username>/', users_db_operations.as_view(), name='user_detail'),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='login'),
    path('products/',productView.as_view(),name='productView'),
    path('cart/',CartItems.as_view(),name='CartItems'),
    path('confirm-order/',ConfirmOrder.as_view(), name='ConfirmOrder'),
    path('orders-count/', OrdersCount.as_view(), name='OrdersCount'),
    path('orders-total-amount/', orders_total_amount, name='orders_total_amount'),
    path('fetch-order-data/', fetch_order_data, name='fetch_order_data'),
    path('custom-order/',CustomOrder.as_view(),name='custom-order'),
]
