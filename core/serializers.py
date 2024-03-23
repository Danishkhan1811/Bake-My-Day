from rest_framework import serializers
from .models import UserModels

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModels
        fields = ['username', 'password', 'email_id', 'birthday']
