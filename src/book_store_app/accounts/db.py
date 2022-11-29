# DB
from django.db import connection
from django.db import IntegrityError

def insert_customer(fname, lname, email, gender, phone, address, zip, subscription, subscrition_start_date):
    
    try:
        with connection.cursor() as cursor:
            
            print('Inserting new customer information to CUSTOMER table')
            add_customer = ("INSERT INTO CUSTOMER "
                    "(First_Name, Last_Name, Email, Gender, Phone, Address, Zipcode, Subscription_ID, Subscription_Start_Date) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

            customer = (fname, lname, email, gender, phone, address, zip, int(subscription), subscrition_start_date)


            cursor.execute(add_customer, customer)
            customer_id = cursor.lastrowid
    
    except IntegrityError as e:
        print('Error occurred')
        print(e)
        return -1
    return customer_id

def insert_login_info(customer_id, password):
    
    with connection.cursor() as cursor:
        print('Inserting new login information to LOGIN table')
        
        add_login = (
                    "INSERT INTO LOGIN "
                    "(Customer_ID, Password) "
                    "VALUES(%s, %s)"
                    )
        login = (customer_id, password)
        
        cursor.execute(add_login, login)
    
    
def check_if_user_is_valid(email, password):
    
    with connection.cursor() as cursor:
        print('Checking if the entered username and password is correct')
        
        select_query =  """
                            SELECT count(*)
                            FROM CUSTOMER c
                            JOIN LOGIN l
                            ON l.CUSTOMER_ID = c.ID
                            WHERE c.EMAIL = %s
                            AND l.PASSWORD = %s
                        """
        
        cursor.execute(select_query, (email, password))
        query_results = cursor.fetchall()
        if query_results[0][0] > 0:
            return True
        
    return False


def get_customer_id(email):
    print(email)
    
    with connection.cursor() as cursor:
        print('Getting customer_id of the user')
        
        select_query =  """
                            SELECT ID
                            FROM CUSTOMER c
                            WHERE c.EMAIL = %(email)s
                        """
        
        cursor.execute(select_query, {'email': email})
        query_results = cursor.fetchall()
        user_id = query_results[0][0]
        return user_id
        
    return -1