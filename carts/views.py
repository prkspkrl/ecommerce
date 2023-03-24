from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from .models import Wish, WishList
from store.models import Product

#save data in session id
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart= request.session.create()
    return cart


def add_to_cart(request, product_id): #function internal
    current_user = request.user
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart,user=current_user)
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity =1,
            cart = cart,
            user = current_user
        )
        cart_item.save()
    return redirect('cart')

def decrease_cart(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item= CartItem.objects.filter(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')



def cart(request, total_one = 0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id =_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total_one += (cart_item.product.discount_price * cart_item.quantity)
            tax  = (total_one*13/100)
            grand_total = (total_one+tax)
            # quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        'total_one':total_one,
        # 'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,

    }
    return render(request, 'store/cart.html',context)

def checkout(request, total_one = 0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id =_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total_one += (cart_item.product.discount_price * cart_item.quantity)
            tax  = (total_one*13/100)
            grand_total = (total_one+tax)
    except ObjectDoesNotExist:
        pass

    context = {
        'total_one':total_one,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,

    }
    return render(request, 'store/checkout.html',context)


#save data in session id
def _wish_id(request):
    wish = request.session.session_key
    if not wish:
        wish= request.session.create()
    return wish

def add_wishlist(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    try:
        wish = Wish.objects.get(wish_id=_wish_id(request))
    except Wish.DoesNotExist:
        wish = Wish.objects.create(
            wish_id=_wish_id(request)
        )
        wish.save()
    try:
        wish_item = WishList.objects.get(product=product,wish=wish,user=current_user)
        wish_item.save()
    except WishList.DoesNotExist:
        wish_item = WishList.objects.create(
            product = product,
            wish = wish,
            user = current_user
        )
        wish_item.save()
    return redirect('store')
    # return render(request,'store/wishlist.html')


def wish(request, wish_items=None):
    try:
        wish = Wish.objects.get(wish_id=_wish_id(request))
        wish_items = WishList.objects.filter(wish=wish, is_active=True)
    except ObjectDoesNotExist:
        pass

    context = {
        'wish_items': wish_items,
    }
    return render(request, 'store/wishlist.html', context)

def clear_wishlist(request):
    return render(request, 'store/wishlist.html', context)