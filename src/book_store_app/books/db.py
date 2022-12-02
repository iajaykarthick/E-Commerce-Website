# DB
from django.db import connection
from django.db import IntegrityError

def add_to_cart(book_isbn, user_id, quantity):
 
    try:
        with connection.cursor() as cursor:
            
            # add_to_cart = ("INSERT INTO Cart "
            #         "(Customer_ID, ISBN, Quantity) "
            #         "VALUES (%s, %s, %s)")

            # cart = (user_id, book_isbn, quantity)
            # cursor.execute(add_to_cart, cart)
            
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

def cart_details(user_id, sort=False, asc=True):

    try:
        with connection.cursor() as cursor:
            
            print("Showing the cart of the particular customer")
            cart_details = (f'''
                            select c.ISBN,b.image,b.title,c.quantity,b.price from book b
                            join cart c
                            on c.ISBN = b.ISBN
                            where c.Customer_ID = {user_id} 
                        ''')
            if sort:
                cart_details += " ORDER BY b.price * c.quantity"
                if asc == False:
                    cart_details += " DESC"
                else:
                    cart_details += " ASC"
                    
            
            print(cart_details)

            cursor.execute(cart_details)
            query_results = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            print(columns)
            cart = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(query_results)]
            
    
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1
    return cart


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