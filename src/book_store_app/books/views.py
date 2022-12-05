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

#list of views
# 1. book_list
# 2. book_detail
# 3. get_cart_details

@my_login_required
def book_list(request):
    
    user_id= request.session['user_id']
    
    show_msg = False
    alert_msg = ""
    
    search = False
    search_col = None
    search_val = None
    
    stores = get_stores(user_id)
    if 'store_id' not in request.session:
        request.session['store_id'] = stores[0]['store_id']
    
    if request.method == 'POST':
        
        action = request.POST['action']
        
        if action == 'addtocart':
            
            show_msg = True
            
            isbn = request.POST['ISBN']
            current_quantity = request.POST['current_quantity'] 
            new_quantity = request.POST['quantity'] 
            
            if new_quantity != current_quantity and int(new_quantity) > 0:
                result = db.add_to_cart(isbn, user_id, new_quantity)
                alert_msg = "Added to Cart" if result == 1 else "Not Added to Cart"
            else:
                alert_msg = "Increase or Decrease Quantity and then add to cart"
                
        elif action == 'search':
            
            search_col = request.POST['search_parameter']
            search_val = request.POST['search_value']
            
            if search_col and search_val:
                print('X ', search_col, search_val)
                search = True
            elif not search_col and search_val:
                show_msg = True
                alert_msg = "Select a column to search on"
                
        elif action == 'changestore':
            store_id = request.POST['store_id']
            if store_id:
                print('Adding to session', store_id)
                request.session['store_id'] = store_id
                
    if search:
        books_list = db.search(user_id, search_col, search_val)
    else:
        books_list = db.getAllBooks(user_id)
        
    if len(books_list) == 0:
        show_msg = True
        alert_msg = "No rows returned"
    
    p = Paginator(books_list, 10)
    page = request.GET.get('page')
    books = p.get_page(page)
    
    context = {
         'books_list':books_list,
         'books': books,
         'request': request,
         'cart_count': db.countCart(user_id),
         'show_msg': show_msg,
         'alert_msg': alert_msg,
         'stores': stores,
         'search': search
    }
    
    return render(request,'books/books_list.html',context)
    
    
@my_login_required
def book_detail(request, isbn):
    cart_added = False
    user_id= request.session['user_id']
    
    
    if request.method == 'POST':
        isbn = request.POST['ISBN']
        quantity = int(request.POST['quantity']) or 1
        
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

@my_login_required
def get_cart_details(request):
    
    sort = False
    if request.method == 'POST' and 'asc' in request.POST:
        if request.POST['asc'] == "False":
            asc = False
        else:
            asc = True
    else:
        asc = True
    user_id = request.session['user_id']
            
    stores = get_stores(user_id)
    if 'store_id' not in request.session:
        request.session['store_id'] = stores[0]['store_id']
    
    store_id = request.session['store_id']
    
    show_msg = False
    alert_msg = ""
    
    if request.method == 'POST':
        print(request.POST)
        action = request.POST['action']
        if action == 'sort':            
            sort = True
        elif action == 'delete_cart_item':
            isbn = request.POST['ISBN']
            db.deleteCartItem(user_id, isbn)
        elif action == 'inc' or action == 'dec':
            print(request.POST)
            isbn = request.POST['ISBN']
            if action == 'inc':
                db.increment_cart(user_id, isbn)
            else:
                db.decrement_cart(user_id, isbn)
                
        elif action == 'payment':
            payment_type = request.POST['payment_type']
            store_id = request.session['store_id']
            payment_id = orders_db.add_order_items(user_id, payment_type, store_id)
            response = redirect('orders:view_order_receipt', payment_id)
            return response

        elif action == 'changestore':
            store_id = request.POST['store_id']
            if store_id:
                print('Adding to session', store_id)
                request.session['store_id'] = store_id
            
    context = {}

    (cart_details, checkout_btn_disable) =db.cart_details(user_id, store_id, sort, asc)
    if checkout_btn_disable:
        show_msg = True
        alert_msg = "Delete the out of stock items to proceed"
   
    context['items'] = cart_details
    context['count_items'] = len(cart_details)
    context['cart_count'] = db.countCart(user_id)
    context['total_cost'] = db.getTotalCartCost(user_id)
    context['asc'] = False if asc and 'asc' in request.POST else True
    context['checkout_btn_disable'] = checkout_btn_disable
    context['show_msg'] = show_msg
    context['alert_msg'] = alert_msg
    context['stores'] = stores
    
    return render(request, 'books/cart.html', context)




def get_stores(user_id):
    # get store_ids 
    results = db.getStores(user_id)
    stores = [{'store_id': store['store_id'], 'store': store['Store_Address']} for store in results]
    return stores


def charts(request):
    result = db.get_user_types()
    context={}
    temp1=[]
    temp2=[]
    titles=[]
    sold_count=[]
    dates=[]
    sales=[]
    month=[]
    monthly_sales=[]
    genre=[]
    book_count=[]
    store_id=[]
    copies_sold=[]
    for i in result:
        temp1.append(i[0])
        temp2.append(i[1])
    result = db.get_top_sold_books()
    for i in result:
        titles.append(i[0])
        sold_count.append(i[1])
    result=db.get_sale_last_5_days()
    for i in result:
        dates.append(str(i[0]))
        sales.append(i[1])
    result=db.monthly_rev()
    for i in result:
        month.append(str(i[0]))
        monthly_sales.append(i[1])

    result=db.popular_genre()
    for i in result:
        genre.append(i[0])
        book_count.append(i[1])


    result = db.store_best_performing()
    for i in result:
        store_id.append(i[0])
        copies_sold.append(i[1])


    context['ids']=temp1
    context['count']=temp2
    context['titles']=titles
    context['sold_count']=sold_count
    context['dates']=dates
    context['sales']=sales
    context['month']=month
    context['monthly_sales']=monthly_sales
    context['genre']=genre
    context['book_count']=book_count
    context['store_id']=store_id
    context['copies_sold']=copies_sold
    print(context)
    return render(request, 'books/charts.html',context)