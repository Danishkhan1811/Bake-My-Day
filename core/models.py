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
    image = models.ImageField(upload_to='assets/',null=True, blank=True)
    price = models.IntegerField()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def total_price(self):
        return self.quantity * self.product.price
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    cart_item_id = models.IntegerField()
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.IntegerField(default=0)
    user_id = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    customer_name = models.CharField(max_length=250, default=0)
    contact = models.CharField(max_length=10,default=0)
    address = models.TextField(default=5)
