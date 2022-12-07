# View 1 - Book Description View

create view some_view as 
SELECT b.*, a.Author_Name, g.Genre 
FROM BOOK b 
JOIN AUTHOR_BOOK ab 
ON b.ISBN = ab.ISBN 
JOIN AUTHOR a 
ON a.AUTHOR_ID = ab.AUTHOR_ID 
JOIN BOOK_GENRE bg 
on b.ISBN = bg.ISBN
JOIN GENRE g
ON bg.GENRE_ID = g.GENRE_ID;

# View 2 - Orders

create view orders_view as 
SELECT O.ORDER_ID, O.PAYMENT_ID, O.TOTAL_PRICE, DATE_FORMAT(O.ORDER_DATE, "%%m/%%d/%%Y") AS ORDER_DATE, 
OI.ISBN, OI.NUMBER_OF_COPIES as quantity, B.title, B.image, (b.price * OI.NUMBER_OF_COPIES) as item_total_price, p.payment_type
FROM PAYMENT P
JOIN ORDERS O
ON P.PAYMENT_ID = O.PAYMENT_ID
JOIN ORDER_ITEMS OI
ON O.ORDER_ID = OI.ORDER_ID
JOIN BOOK B
ON OI.ISBN = B.ISBN
JOIN CUSTOMER C
ON O.CUSTOMER_ID = C.ID;
