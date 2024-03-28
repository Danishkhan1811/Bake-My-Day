from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True)

# Signal to create UserDetails object when a new User is created
@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)

# Signal to save UserDetails object when a User is saved
@receiver(post_save, sender=User)
def save_user_details(sender, instance, **kwargs):
    instance.userdetails.save()

# class Products(models.Model):
#     from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    image_path = models.CharField(max_length=255)

