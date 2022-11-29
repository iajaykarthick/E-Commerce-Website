# DB
from django.db import connection
from django.db import IntegrityError

def add_to_cart(book_isbn,email,quantity):
 
    try:
        with connection.cursor() as cursor:
            
            print(email)
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