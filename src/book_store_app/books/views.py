from django.http import HttpResponse
from urllib.parse import urlencode
from django.urls import reverse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from . import db as db
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
    cursor = connection.cursor()
    
    if request.method == 'POST':
        print(f'Request is {request.POST}')
            
        isbn = request.POST['ISBN']
        
        ## Insert into cart table 
        email= request.session['user_id']
        result = db.add_to_cart(isbn,email, 1)
        if result == 1:
            cart_added = True
        
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
         'cart_count': 10,
         'added': cart_added
    }
    
    return render(request,'books/books_list.html',context)
    
    
@my_login_required
def book_detail(request, isbn):
    
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
    
    return render(request, 'books/book_detail.html', {'book': book[0]})

@my_login_required
def add_to_cart(request):

    ## Insert into cart table 
    email=request.session['user_id']
     
    base_url = reverse('books:list')  # 1 /books/
    query_string =  urlencode({'cart_added': True})  # 2 cart_added=True
    url = '{}?{}'.format(base_url, query_string)  # /books/?cart_added=True

    return render(request, 'books/cart.html', {})
    #return redirect(url)
    


@my_login_required
def get_cart_details(request):

    ## Insert into cart table 
    email=request.session['user_id']
    cart_details=db.cart_details(email)
    print("Printing the cart details")
    for i in cart_details:
        print(i)
    return render(request, 'books/cart.html', {})
    #return redirect(url)