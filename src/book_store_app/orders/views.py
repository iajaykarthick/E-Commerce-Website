from django.shortcuts import render, redirect
from . import db
from books import db as books_db
import random


# login required
from book_store_app.decorators import my_login_required

app_name = 'orders'


@my_login_required
def confirmation(request):
    user_id = request.session['user_id']
    payment_id = db.add_order_items(user_id)
    response = redirect('orders:view_order_receipt', payment_id)
    return response
    


@my_login_required
def view_order_receipt(request, payment_id):
    
    user_id = request.session['user_id']
    
    order_items = db.getOrderDetail(payment_id)
    
    print(order_items)
    if len(order_items):
        name = order_items[0]['NAME']
        order_id = order_items[0]['ORDER_ID']
        order_date = order_items[0]['ORDER_DATE']
        total_price = order_items[0]['TOTAL_PRICE']
        total_price_without_shipping = order_items[0]['TOTAL_PRICE'] - 20
        payment_type = order_items[0]['PAYMENT_TYPE']
    else:
        name = None
        total_price = None
        order_id = None
        order_date = None
        total_price_without_shipping = None
        payment_type = None
    
        
    
    context = {
        'name': name,
        'order_id': order_id,
        'order_date': order_date,
        'total_price': total_price,
        'voucher': get_voucher(),
        'total_price_without_shipping': total_price_without_shipping,
        'order_items': order_items,
        'cart_count': books_db.countCart(user_id),
        'payment_type': payment_type
    }
    return render(request, 'orders/order.html', context)
    

@my_login_required
def view_orders(request):
    user_id = request.session['user_id']

    orders = db.getListOfOrdersPlaced(user_id)
    print(orders)
    
    context = {
        'orders': orders,
        'cart_count': books_db.countCart(user_id),
    }
    
    
    
    return render(request, 'orders/orders.html', context)


def get_voucher(num_chars=9):
     code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
     code = ''
     for i in range(0, num_chars):
         slice_start = random.randint(0, len(code_chars) - 1)
         code += code_chars[slice_start: slice_start + 1]
     return code
