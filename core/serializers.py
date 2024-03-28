from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email_id', 'birthday']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id','product_name','description','image_path']

