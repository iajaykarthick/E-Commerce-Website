# DB
from django.db import connection
from django.db import IntegrityError
from django.db import OperationalError

def add_to_cart(book_isbn, user_id, quantity):
 
    try:
        with connection.cursor() as cursor:
            print("Updating Particular cart item from user's cart")
            args = [user_id, book_isbn, quantity]
            result_args = cursor.callproc('cart_update', args)
            print(result_args)
            
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1
    return 1

def countCart(user_id):
    try:
        with connection.cursor() as cursor:
            cart_total = (" SELECT cart_total_qty(%s)")
            cursor.execute(cart_total,[user_id])
            query_results = cursor.fetchall()
            count_cart = query_results[0][0]
            
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1

    return count_cart or 0


def getTotalCartCost(user_id):
    
    try:
        with connection.cursor() as cursor:
            cart_total = (" SELECT cart_total_charge(%s)")
            cursor.execute(cart_total, [user_id])
            query_results = cursor.fetchall()
            total_cost = query_results[0][0]
            
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1

    return total_cost or 0

def cart_details(user_id, store_id, sort=False, asc=True):

    try:
        with connection.cursor() as cursor:
            checkout_btn_disable = False
            print("Showing the cart of the particular customer")
            cart_details = (f'''
                            SELECT c.ISBN,b.image,b.title,c.quantity,b.price from book b
                            JOIN cart c
                            ON c.ISBN = b.ISBN
                            WHERE c.Customer_ID = {user_id} 
                        ''')
            if sort:
                cart_details += " ORDER BY b.price * c.quantity"
                if asc == False:
                    cart_details += " DESC"
                else:
                    cart_details += " ASC"

            cursor.execute(cart_details)
            query_results = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            print(columns)
            cart = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(query_results)]
            
            for book in cart:
                book['isAvailable'] = ifCopiesAvailale(book['ISBN'], book['quantity'], store_id)
                if book['isAvailable'] == 0:
                    checkout_btn_disable = True
    
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1
    return (cart, checkout_btn_disable)

def ifCopiesAvailale(isbn, qty, store_id):
    try:
        with connection.cursor() as cursor:
            cart_total = (" SELECT check_copies_present(%s, %s, %s)")
            cursor.execute(cart_total, [store_id, isbn, qty])
            query_results = cursor.fetchall()
            availableornot = query_results[0][0]
            
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1

    return availableornot or 0

def deleteCartItem(user_id, isbn):
    try:
        with connection.cursor() as cursor:
            
            print("Deleting Particular cart item from user's cart")
            args = (user_id, isbn, 0)
            result_args = cursor.callproc('delete_book_cart', args)
            print(result_args)
            

    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1

    return 1


def getStores(user_id):
    try:
        with connection.cursor() as cursor:
            
            cursor.callproc('store_location', (user_id, ))
            result_args = cursor.fetchall()
            
            columns = [col[0] for col in cursor.description]
            stores = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(result_args)]
            
            return stores
        
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1
    
def getAllBooks(user_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                                SELECT B.*, C.QUANTITY 
                                FROM BOOK B 
                                LEFT JOIN (SELECT * FROM CART WHERE CUSTOMER_ID = %(user_id)s) C
                                ON B.ISBN = C.ISBN;
                            ''', {'user_id' : user_id})

            query_results = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            books = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(query_results)]
            
            return books
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1


def search(user_id, search_col, search_val):
    procedure = {
        'isbn': 'books_with_ISBN',
        'title': 'books_name',
        'author': 'books_with_author',
        'genre': 'books_with_genre',
        'year': 'books_with_year',
        'publisher': 'books_with_publisher'
    }
    
    try:
        with connection.cursor() as cursor:
            
            cursor.callproc(procedure[search_col], (search_val, user_id, ))
            result_args = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            books = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(result_args)]        
            return books
    
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1

def increment_cart(user_id, isbn):
    try:
        with connection.cursor() as cursor:
            print(user_id, isbn)
            result_args = cursor.callproc('inc_qty', (user_id, isbn))
            print(result_args)
    
    except OperationalError as e:
        print(e)
        return -1
    
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1
    
    
def decrement_cart(user_id, isbn):
    try:
        with connection.cursor() as cursor:
            print(user_id, isbn)
            result_args = cursor.callproc('dec_qty', (user_id, isbn))
            print(result_args)
    
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1


def get_user_types():
    try:
        with connection.cursor() as cursor:
            print("geting user types")
            cursor.execute('''select Subscription_ID,count(*) from Customer
                                group by Subscription_ID''')
            result =  cursor.fetchall()
            return result
    
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1 
    



def get_top_sold_books():
    try:
        with connection.cursor() as cursor:
            print("geting top sold books")
            cursor.execute('''select b.title,sum(number_of_copies) 
                                from order_items o
                                join book b
                                on b.ISBN = o.ISBN
                                group by o.ISBN
                                order by sum(number_of_copies) desc 
                                limit 5 ''')
            result =  cursor.fetchall()
            return result
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1 

def get_sale_last_5_days():
    try:
        with connection.cursor() as cursor:
            print("Last 5 days sale")
            cursor.execute('''select order_date, sum(Total_Price) from orders
                                group by order_date
                                limit 5''')
            result =  cursor.fetchall()
            return result
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1 

def monthly_rev():
    try:
        with connection.cursor() as cursor:
            print("Montly Revenue for current year")
            cursor.execute('''select month(order_date) as 'month', sum(Total_Price) as 'Total_Revenue per month'
                            from orders
                            where year(order_date) = year(CURRENT_TIMESTAMP)
                            group by month(order_date)
                            ''')
            result =  cursor.fetchall()
            return result
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1 

def popular_genre():
    try:
        with connection.cursor() as cursor:
            print("Most Popular Genres")
            cursor.execute('''
                                select g.Genre,count(*) from ORDER_ITEMS o
                                join BOOK_GENRE bg on bg.ISBN= o.ISBN
                                join Genre g on g.Genre_ID =  bg.Genre_ID
                                group by g.Genre_ID
                                order by count(*) desc
                                limit 5
                            ''')
            result =  cursor.fetchall()
            return result
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1 

def store_best_performing():
    try:
        with connection.cursor() as cursor:
            print("Best Performing Store")
            cursor.execute('''
                               select Store_ID,count(*) as cnt from ORDERS 
                                group by Store_ID 
                                order by cnt desc 
                                limit 5
                            ''')
            result =  cursor.fetchall()
            return result
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1 
