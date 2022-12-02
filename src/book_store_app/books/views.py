from django.http import HttpResponse
from urllib.parse import urlencode
from django.urls import reverse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from . import db as db
from orders import db as orders_db
# DB
from django.db import connection

# pagination
from django.core.paginator import Paginator

# login required
from book_store_app.decorators import my_login_required


app_name = 'books'

@my_login_required
def book_list(request):
    
    cart_added = False
    alert_msg = ""
    cursor = connection.cursor()
    user_id= request.session['user_id']
    if request.method == 'POST':
        print(f'Request is {request.POST}')
        isbn = request.POST['ISBN']
        current_quantity = request.POST['current_quantity'] 
        new_quantity = request.POST['quantity'] 
        ## Insert into cart table 
        cart_added = True
        if new_quantity != current_quantity and int(new_quantity) > 0:
            result = db.add_to_cart(isbn, user_id, new_quantity)
            if result == 1:
                
                alert_msg = "Added to Cart"
            else:
                
                alert_msg = "Not Added to Cart"
        else:
            
            alert_msg = "Increase or Decrease Quantity and then add to cart"
            
    # cursor.execute('SELECT * FROM BOOK')
    
    cursor.execute('''
                    SELECT B.*, C.QUANTITY 
                    FROM BOOK B 
                    LEFT JOIN (SELECT * FROM CART WHERE CUSTOMER_ID = 1001) C
                    ON B.ISBN = C.ISBN;
                   ''')

    query_results = cursor.fetchall()
    
    columns = [col[0] for col in cursor.description]
    print(columns)
    books_list = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(query_results)]
    
    # set up pagination
    p = Paginator(books_list, 10)
    page = request.GET.get('page')
    books = p.get_page(page)
    
    context = {
         'books_list':books_list,
         'books': books,
         'request': request,
         'cart_count': db.countCart(user_id),
         'added': cart_added,
         'alert_msg': alert_msg
    }
    
    return render(request,'books/books_list.html',context)
    
    
@my_login_required
def book_detail(request, isbn):
    cart_added = False
    user_id= request.session['user_id']
    if request.method == 'POST':
        isbn = request.POST['ISBN']
        quantity = int(request.POST['quantity']) or 1
        print(quantity)
        ## Insert into cart table 
        result = db.add_to_cart(isbn, user_id, quantity)
        if result == 1:
            cart_added = True
    cursor = connection.cursor()
    cursor.execute(f'''
                    SELECT b.*, a.Author_Name, g.Genre 
                    FROM BOOK b JOIN AUTHOR_BOOK ab 
                    ON b.ISBN = ab.ISBN 
                    JOIN AUTHOR a 
                    ON a.AUTHOR_ID = ab.AUTHOR_ID 
                    JOIN BOOK_GENRE bg 
                    on b.ISBN = bg.ISBN
                    JOIN GENRE g
                    ON bg.GENRE_ID = g.GENRE_ID
                    WHERE b.ISBN = {isbn}''')

    query_results = cursor.fetchall()
    
    columns = [col[0] for col in cursor.description]
    print(columns)
    book = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(query_results)]
    
    authors = list(set([b['Author_Name'] for b in book]))
    genres = list(set([b['Genre'] for b in book]))
    
    book[0]['author'] = ', '.join(authors)
    book[0]['genres'] = ', '.join(genres)
    
    return render(request, 'books/book_detail.html', {
                                                    'book': book[0],
                                                    'cart_count': db.countCart(user_id),
                                                    'added': cart_added
                                                    })

# @my_login_required
# def add_to_cart(request):

#     ## Insert into cart table 
#     email=request.session['user_id']
     
#     base_url = reverse('books:list')  # 1 /books/
#     query_string =  urlencode({'cart_added': True})  # 2 cart_added=True
#     url = '{}?{}'.format(base_url, query_string)  # /books/?cart_added=True

#     return render(request, 'books/cart.html', {})
#     #return redirect(url)
    


@my_login_required
def get_cart_details(request):
    print(request.method)
    sort = False
    if request.method == 'POST' and 'asc' in request.POST:
        if request.POST['asc'] == "False":
            asc = False
        else:
            asc = True
    else:
        asc = True
    
    user_id = request.session['user_id']
    print("USER ID",user_id)
    if request.method == 'POST':
        print(request.POST)
        action = request.POST['action']
        if action == 'sort':            
            sort = True
        elif action == 'delete_cart_item':
            isbn = request.POST['ISBN']
            db.deleteCartItem(user_id, isbn)
        elif action == 'payment':
            payment_type = request.POST['payment_type']
            payment_id = orders_db.add_order_items(user_id, payment_type)
            response = redirect('orders:view_order_receipt', payment_id)
            return response
            
    context = {}

    cart_details=db.cart_details(user_id, sort, asc)
    print(cart_details)
   
    context['items'] = cart_details
    context['count_items'] = len(cart_details)
    context['cart_count'] = db.countCart(user_id)
    context['total_cost'] = db.getTotalCartCost(user_id)
    context['asc'] = False if asc and 'asc' in request.POST else True
    
    return render(request, 'books/cart.html', context)