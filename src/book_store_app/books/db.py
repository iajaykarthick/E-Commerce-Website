# DB
from django.db import connection
from django.db import IntegrityError

def add_to_cart(book_isbn,email,quantity):
 
    try:
        with connection.cursor() as cursor:
            
            user=(" SELECT  ID from Customer where EMAIL =(%s)")
            cursor.execute(user,[email])
            query_results = cursor.fetchall()
            user_id = query_results[0][0]
            print(user_id)
            print("Inserting the customer id, isbn of the book they added to cart ")
            add_to_cart = ("INSERT INTO Cart "
                    "(Customer_ID, ISBN, Quantity) "
                    "VALUES (%s, %s, %s)")

            cart = (user_id, book_isbn, quantity)
            cursor.execute(add_to_cart, cart)
            
    
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1
    return 1



def cart_details(email):
 
    try:
        with connection.cursor() as cursor:
            
            user=(" SELECT  ID from Customer where EMAIL =(%s)")
            cursor.execute(user,[email])
            query_results = cursor.fetchall()
            user_id = query_results[0][0]
            print(user_id)
            print("Showing the cart of the particular customer")
            cart_details = (f'''select c.ISBN,b.image,b.title,b.price from book b
                            join cart c
                            on c.ISBN = b.ISBN
                            where c.Customer_ID = {user_id} ''')

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