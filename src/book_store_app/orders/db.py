# DB
from django.db import connection
from django.db import IntegrityError


def add_order_items(user_id, payment_type):
 
    try:
        with connection.cursor() as cursor:
            print("calling checkout procedure")
            args = (user_id, payment_type, 0)
            cursor.callproc('checkout', args)
            cursor.execute("select @_checkout_2")
            result =  cursor.fetchall()
            return result[0][0]
    
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1
    
    
def getOrderDetail(payment_id):
    
    try:
        with connection.cursor() as cursor:
            print("Getting Order Details")
            select_query = """
                            SELECT CONCAT(C.FIRST_NAME, ' ', C.LAST_NAME) AS NAME, O.ORDER_ID, O.TOTAL_PRICE, DATE_FORMAT(O.ORDER_DATE, '%%m/%%d/%%Y') AS ORDER_DATE, OI.ISBN, OI.NUMBER_OF_COPIES as quantity, B.title, B.image, (b.price * OI.NUMBER_OF_COPIES) as item_total_price,
                            CASE
                                WHEN p.PAYMENT_TYPE = 1 THEN 'Card'
                                WHEN p.PAYMENT_TYPE = 2 THEN 'Paypal'
                                ELSE 'Cash On Delivery'
                            END AS PAYMENT_TYPE
                            FROM PAYMENT P
                            JOIN ORDERS O
                            ON P.PAYMENT_ID = O.PAYMENT_ID
                            JOIN ORDER_ITEMS OI
                            ON O.ORDER_ID = OI.ORDER_ID
                            JOIN BOOK B
                            ON OI.ISBN = B.ISBN
                            JOIN CUSTOMER C
                            ON O.CUSTOMER_ID = C.ID
                            WHERE P.PAYMENT_ID = %(payment_id)s
                           """
            
            cursor.execute(select_query, {'payment_id': payment_id})
            results = cursor.fetchall()
            
            
            columns = [col[0] for col in cursor.description]
            print(columns)
            res = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(results)]
            print(res)
            return res
    
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1
    
def getListOfOrdersPlaced(user_id):
    try:
        with connection.cursor() as cursor:
            print("Getting list of Order Details")
    
            select_query = """
                    SELECT O.ORDER_ID, O.TOTAL_PRICE, DATE_FORMAT(O.ORDER_DATE, "%%m/%%d/%%Y") AS ORDER_DATE, OI.ISBN, OI.NUMBER_OF_COPIES as quantity, B.title, B.image, (b.price * OI.NUMBER_OF_COPIES) as item_total_price, p.payment_type
                    FROM PAYMENT P
                    JOIN ORDERS O
                    ON P.PAYMENT_ID = O.PAYMENT_ID
                    JOIN ORDER_ITEMS OI
                    ON O.ORDER_ID = OI.ORDER_ID
                    JOIN BOOK B
                    ON OI.ISBN = B.ISBN
                    JOIN CUSTOMER C
                    ON O.CUSTOMER_ID = C.ID
                    WHERE C.ID = %(user_id)s
                    ORDER BY O.ORDER_ID;
                    """
                    
            cursor.execute(select_query, {'user_id': user_id})
            results = cursor.fetchall()
            
            
            columns = [col[0] for col in cursor.description]
            print(columns)
            res = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(results)]
            
            o_id = None
            
            span = {order['ORDER_ID']: 0 for order in res}

            for order in res:
                span[order['ORDER_ID']] += 1 
            print('**********')
            for s in span:
                print(s, span[s])
            print('**********')
            
            
            orders = []
            order = []
            for row in res:
                item = {'span': None}
                if o_id != row['ORDER_ID'] and o_id is not None:
                    o_id = row['ORDER_ID']
                    orders.append(order)
                    order = []
                    item['span'] = span[row['ORDER_ID']]
                elif o_id is None:
                    o_id = row['ORDER_ID']
                    item['span'] = span[row['ORDER_ID']]
                item['order_id'] = row['ORDER_ID']
                item['title'] = row['title']
                item['order_date'] = row['ORDER_DATE']
                item['quantity'] = row['quantity']
                item['image'] = row['image']
                item['item_total_price'] =  row['item_total_price']
                item['total_price'] = row['TOTAL_PRICE']
                order.append(item)
    
            return orders
        
    except IntegrityError as e:
        print("Error occurred")
        print(e)
        return -1