from django.db import models
from store.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Account

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=200, blank=True)
    date_added= models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.discount_price * self.quantity

    def __str__(self):
        return self.product.product_name



class Wish(models.Model):
    wish_id = models.CharField(max_length=200, blank=True)
    date_added= models.DateField(auto_now_add=True)

    def __str__(self):
        return self.wish_id


class WishList(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.discount_price * self.quantity

    def __str__(self):
        return self.product.product_name


# class Checkout(models.Model):
#     full_name = models.CharField(max_length=100)
#     phone_number = PhoneNumberField(help_text='Contact phone number')
#     email       = models.EmailField(max_length=15,null=True)
#     address = models.CharField(max_length=20)
#     address2 = models.CharField(max_length=50,null=True)
#     delivery_day = models.CharField(max_length=20,null=True)
#     note = models.TextField()
#
#     def __str__(self):
#         self.full_name

    