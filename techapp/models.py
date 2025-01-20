from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class Gadget(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     features = models.JSONField(default=list)
#     image= models.ImageField(upload_to='gadgets/')

#     def __str__(self):
#         return self.name

class ContactDetail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()    
    
    def __str__(self):
        return self.name
    
# upadate profile
    
# models.py
# from django.contrib.auth.models import User
# from django.db import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     address = models.TextField(max_length=255, blank=True, null=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
    
#     def __str__(self):
#         return self.user.username
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)  # JSON field to store list
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        # Assuming 'features' is a list
        feature_list = "\n".join([f"• {feature}" for feature in self.features])
        return f"{self.name}\nFeatures:\n{feature_list}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def total(self):
        return self.product.price * self.quantity