from django.contrib import admin
from django.urls import path
from core import views
from .views import users_db_operations

urlpatterns = [
    path('users/', users_db_operations.as_view(), name='users_db_operations'),
    path('users/<int:user_id>/', users_db_operations.as_view(), name='user_detail'),
    path('users/<str:username>/', users_db_operations.as_view(), name='user_detail')
]
