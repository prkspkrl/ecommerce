from django.contrib import admin
from .models import Cart,CartItem
from .models import Wish, WishList
    # Checkout
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wish)
admin.site.register(WishList)
# admin.site.register(Checkout)
