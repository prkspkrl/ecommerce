from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from orders.models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.discount_price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (13 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form =OrderForm(request.POST)
        if form.is_valid():

            data=Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['first_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20230305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'tax': tax,
                'cart_items': cart_items,
                'total': total,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')
    return render(request,'store/checkout.html')


def paypal_test(request):
    return render(request, 'store/paypal_test.html')

def payments(request):
    body = json.loads(request.body)
    # print(body)
    # return HttpResponse(body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    # print(order)

#Store transaction details inside payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    print(payment)
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # 1.Move the cart item to order product table
    cart_items = CartItem.objects.filter(user=request.user)
    # like a= 5
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # 2.reduce the quantity of sold product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # 3.clear the cart
    CartItem.objects.filter(user=request.user).delete()

    # 4.Send email received email to the customer
    mail_subject = 'Thank you for order'
    message = render_to_string('orders/order_receive_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # 5.Send Order number and transaction id back to SendData method via Json Response [Thank you page]
    # send data to payment page
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)
    return render(request, 'orders/payments.html')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)

        subtotal = 0
        tax = 0
        for i in ordered_products:
            subtotal += i.product.discount_price * i.quantity
            tax = (subtotal*13)/100
            grand_total = subtotal+tax

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,  # or simplay order_number gives
            'transID': payment.payment_id,
            'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,

        }
        return render(request, 'orders/order_complete.html', context)


    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')



