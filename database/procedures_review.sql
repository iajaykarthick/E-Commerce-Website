## Stored Procedure 1
# Getting book name with author 
DROP PROCEDURE IF EXISTS books_with_author;
delimiter $$
create procedure books_with_author(
	in author_name varchar(80),
    in customer_id int
)
begin 
	select b.*, C.QUANTITY
	from author a
	join author_book ab on ab.Author_ID = a.Author_ID
	join book b on b.ISBN = ab.ISBN
    LEFT JOIN (SELECT * FROM CART WHERE CUSTOMER_ID = customer_id) C
	ON B.ISBN = C.ISBN
    where a.Author_Name like CONCAT('%',author_name, '%')
;
end $$
delimiter ;

-- call books_with_author('Ajay', 1001);

-- --------------------------------------------- --

## Stored Procedure 2
# Getting book name with publisher name  
DROP PROCEDURE IF EXISTS books_with_publisher;
delimiter $$
create procedure books_with_publisher(
	in publisher_name varchar(80),
    in cid int
)
begin 
	select b.*, C.QUANTITY
	from book b 
	join publisher p on p.Publisher_ID = b.Publisher_ID
    LEFT JOIN (SELECT * FROM CART WHERE CUSTOMER_ID = customer_id) C
	ON B.ISBN = C.ISBN
	where p.Publisher_Name like concat('%',publisher_name,'%');

end $$
delimiter ;

-- call books_with_publisher('HarperPerennial', 1001);
-- call books_with_publisher('Random House');

-- --------------------------------------------- --

## Stored Procedure 3
# Getting book name with Genre  
DROP PROCEDURE IF EXISTS books_with_genre;
delimiter $$
create procedure books_with_genre(
	in genre_name varchar(80),
    in cid int
)
begin 
	select b.*, C.QUANTITY
	from genre g 
	join book_genre bg on bg.Genre_ID = g.Genre_ID
	join book b
	on bg.ISBN = b.ISBN
    LEFT JOIN (SELECT * FROM CART WHERE CUSTOMER_ID = customer_id) C
	ON B.ISBN = C.ISBN
	where g.Genre like concat('%',genre_name,'%');
end $$
delimiter ;

-- call books_with_genre('classic', 1001);

-- --------------------------------------------- --

## Stored procedure 4
## Getting books by ISBN
DROP PROCEDURE IF EXISTS books_with_ISBN;
delimiter $$
create procedure books_with_ISBN(
	in isbn varchar(80),
    in cid int
)
begin 
	select B.*, C.QUANTITY
	FROM book B
    LEFT JOIN (SELECT * FROM CART WHERE CUSTOMER_ID = customer_id) C
	ON B.ISBN = C.ISBN
	where B.ISBN = isbn;
end $$
delimiter ;

-- call books_with_ISBN('0020199090', 1001);
-- select * from BOOK;

-- --------------------------------------------- --

## Stored Procedure 5
# Getting book name year  
DROP PROCEDURE IF EXISTS books_with_year;
delimiter $$
create procedure books_with_year(
	in year_value varchar(80),
    in cid int
)
begin 
	select B.*, C.QUANTITY
	from BOOK B
    LEFT JOIN (SELECT * FROM CART WHERE CUSTOMER_ID = customer_id) C
	ON B.ISBN = C.ISBN
	where Published_Year = year_value;
    
end $$
delimiter ;

-- call books_with_year(2001, 1001);

-- --------------------------------------------- --

# Stored Procedure 6
## Getting books with book name(no need whole name)
DROP PROCEDURE IF EXISTS books_name;
delimiter $$
create procedure books_name(
	in bname varchar(80),
    in cid int
)
begin 
	select B.*, C.QUANTITY
	from BOOK B
    LEFT JOIN (SELECT * FROM CART WHERE CUSTOMER_ID = customer_id) C
	ON B.ISBN = C.ISBN
	where title like concat('%',bname,'%');
end $$
delimiter ;

-- call books_name('walk', 1001);

-- --------------------------------------------- --

# Stored procedure 7
## Updating the cart 
DROP PROCEDURE IF EXISTS cart_update;
delimiter $$
create procedure cart_update(
	in id int, 
    in book_id varchar(10),
    in book_qty int
)
begin 
	declare present_or_not int;
    
	select count(*) into present_or_not
	from cart
	where customer_id = id and ISBN = book_id;
    
    if present_or_not < 1 then 
		insert into cart(Customer_ID, ISBN, Quantity) values(id,book_id,book_qty);
        
	else
		update cart 
        set Quantity = book_qty
        where Customer_ID = id and ISBN = book_id;
        
    end if;

end $$
delimiter ;

-- call cart_update(18,'0030096189',15);
-- select * from cart;

-- --------------------------------------------- --

## Stored Procedure 8
## PROCEDURE TO INSERT PAYMENT, ORDER INFORMATION
DROP PROCEDURE IF EXISTS checkout;
delimiter $$
CREATE PROCEDURE checkout(
	in customer_id int, 
    in payment_type int,
    in store_id int,
    out p_id int
)
BEGIN
    
    INSERT INTO PAYMENT(PAYMENT_TYPE) VALUES(payment_type);
    SET @payment_id = LAST_INSERT_ID();
    SET p_id := LAST_INSERT_ID();
    SET @s_id := store_id;
    
    INSERT INTO ORDERS(Customer_ID, Total_Price, Payment_ID, STORE_ID)
	SELECT c.CUSTOMER_ID, sum(c.quantity * b.price) + 20, @payment_id, @s_id
	FROM CART c
	JOIN Book b on c.ISBN=b.ISBN
	WHERE c.CUSTOMER_ID= customer_id
    GROUP BY c.CUSTOMER_ID;
    
    SET @order_id = LAST_INSERT_ID();
    
	INSERT INTO ORDER_ITEMS
	SELECT @order_id, c.ISBN, c.quantity
	FROM CART c
	WHERE c.Customer_ID= customer_id; 

	DELETE FROM cart where Customer_ID = customer_id;
    
    
END $$
delimiter ;
select * from orders;
-- select * from store_copies where store_id = 1;

-- CALL checkout(1001, 1, 2, @M);

-- SELECT * FROM ORDERS;
-- select * from cart;
-- SELECT @M;
 
 -- --------------------------------------------- --
 
### Stored Procedure 9
### Procedure to increase the cart value by one 
DROP PROCEDURE IF EXISTS inc_qty;
delimiter $$
create procedure inc_qty(
cid int,
book_isbn varchar(10))

begin 
	declare no_of_copies int;
    
	select Quantity into no_of_copies
	from cart
	where Customer_ID = cid and ISBN = book_isbn;
    
	UPDATE cart
	SET Quantity = no_of_copies + 1
	WHERE Customer_ID = cid and ISBN = book_isbn;
	
end $$
delimiter ;

-- call inc_qty(1,'0002005018');
-- select * from cart;

-- --------------------------------------------- --

 ### Stored Procedure 10
### Procedure to decrease the quantity by 1 of book
DROP PROCEDURE IF EXISTS dec_qty;
delimiter $$
create procedure dec_qty(
cid int,
book_isbn varchar(10))

begin 
	declare no_of_copies int;
    
	select Quantity into no_of_copies
	from cart
	where Customer_ID = cid and ISBN = book_isbn;
    
	UPDATE cart
	SET Quantity = no_of_copies - 1
	WHERE Customer_ID = cid and ISBN = book_isbn;
	
end $$
delimiter ;

-- call dec_qty(1,'0002005018');
-- select @val;
-- select * from cart;

-- --------------------------------------------- --

### Stored Procedure 11
# procedure to delete row from cart (removing product from cart)
# tried function but not giving proper output 

DROP PROCEDURE IF EXISTS delete_book_cart;
delimiter $$
create procedure delete_book_cart(
    in cid int,
    in book_isbn char(10),
    out note varchar(50)
)
begin 
    delete from cart 
    where cart.Customer_ID = cid and cart.ISBN = book_isbn;
    set note = 'Removed Book Sucessfully';
    
end $$
delimiter ;

-- insert into cart values(1,'0002005018',4);
-- select * from cart;

-- call delete_book_cart(1,'0002005018',@val);
-- select @val;

-- select * from cart;

-- delete from cart 
-- where Customer_ID = 5;



## Stored Procedure 12
#### Procedure to get the locaions of the store based on the user location 
## This will give us store id of the 10 store present in that state.

delimiter $$
create procedure store_location(
	in cid int
)
begin 

	with customer_details as (select z.State
							  from customer c 
							  join zipcode z 
							  on z.zipcode = c.zipcode
							  where c.id = cid), # here you should give id of the customer.

	store_details as (select z.zipcode, s.store_id, s.Store_Address,z.city, z.state
					  from store s 
					  join zipcode z 
					  on z.zipcode = s.zipcode
					  join customer_details cd 
					  on cd.state = z.state)

	select z.zipcode, s.store_id, s.Store_Address ,z.City, z.State
    from customer c 
    join zipcode z 
    on z.zipcode = c.zipcode
    join store s on s.Zipcode= z.zipcode
    where c.id = cid
    
	union 
    
	select * from store_details 
	order by store_id
	limit 9;
    
end $$
delimiter ;

call store_location(18);

