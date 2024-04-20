from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product, Cart, Orders

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email_id', 'birthday']

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Product
        fields = ['product_id','product_name','description','image','price']
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product_id','product_name','user_id','quantity','created_at','ordered']

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ['order_id','cart_item_id','user_id','order_date','amount','product_id','customer_name','contact','address']
