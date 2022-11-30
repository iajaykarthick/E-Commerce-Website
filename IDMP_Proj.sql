### Triggers 
#Trigger for checking user does not enter more than 10 quantity.

delimiter $$

CREATE TRIGGER  check_quantity_max_limit  BEFORE INSERT ON CART

FOR EACH ROW

BEGIN

IF NEW.quantity >10 THEN

SIGNAL SQLSTATE '45000'

SET MESSAGE_TEXT = 'ERROR:

         Max BookQuantity MUST BE 10!';

END IF;

END $$

delimiter ;

show triggers;


select * from cart;

insert into cart values(1,'0061030147',15 );


## 1 STored Procedure 
# Getting book name with author 

delimiter $$
create procedure books_with_author(
	in author_name varchar(80) 
)
begin 
	select b.*
	from author a
	join author_book ab on ab.Author_ID = a.Author_ID
	join book b on b.ISBN = ab.ISBN
    where a.Author_Name like CONCAT('%',author_name, '%')
;
end $$
delimiter ;

call books_with_author('helprin');


## 2nd Stored Procedure 
# Getting book name with publisher name  

delimiter $$
create procedure books_with_publisher(
	in publisher_name varchar(80) 
)
begin 
	select b.*
	from book b 
	join publisher p on p.Publisher_ID = b.Publisher_ID
	where p.Publisher_Name like concat('%',publisher_name,'%');

end $$
delimiter ;

call books_with_publisher('HarperPerennial');
call books_with_publisher('Random House');


## 3rd Procedure
# Getting book name with Genre  

delimiter $$
create procedure books_with_genre(
	in genre_name varchar(80) 
)
begin 
	select b.*
	from genre g 
	join book_genre bg on bg.Genre_ID = g.Genre_ID
	join book b
	on bg.ISBN = b.ISBN
	where g.Genre like concat('%',genre_name,'%');
end $$
delimiter ;

call books_with_genre('classic');


## 4th procedure 
# Getting book name year  

delimiter $$
create procedure books_with_year(
	in year_value varchar(80) 
)
begin 
	select *
	from book
	where Published_Year = year_value;
    
end $$
delimiter ;

call books_with_year(2001);


# 5th procedure
## Getting books with book name(no need whole name)

delimiter $$
create procedure books_name(
	in bname varchar(80) 
)
begin 
	select * 
	from book
	where title like concat('%',bname,'%');
end $$
delimiter ;

call books_name('walk');


# 6th procedure 
## Updating the cart 

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
        set Quantity = Quantity+book_qty
        where Customer_ID = id and ISBN = book_id;
        
    end if;

end $$
delimiter ;

call cart_update(18,'0030096189',15);
select * from cart;
 
### Functions 

## Add your your customer_id 
insert into cart(Customer_ID, ISBN, Quantity) values(1,'0002005019',1); 
insert into cart(Customer_ID, ISBN, Quantity) values(1,'0020199090',10);


# Function 1 
# Function to check the quantity of qart 
delimiter $$ 
create function cart_total_qty(cid int)
returns int 
deterministic
begin
	
    declare cartsum int;
    
    select sum(Quantity) into cartsum
	from cart
	where Customer_ID = cid
	group by Customer_ID;
	
    return cartsum;
    
end $$
delimiter ;

select cart_total_qty(18);


## Function 2
## Function to check login 
delimiter $$
create function login(email_id varchar(80),pass varchar(100))
returns int 
deterministic 
begin 
	declare login_validity int;
    
	select count(*) into login_validity
	from CUSTOMER c
	join LOGIN l
	on l.CUSTOMER_ID = c.ID
	WHERE c.EMAIL = email_id and l.Password = pass;
    
    return login_validity;
    
end $$
delimiter ;
    
select login('nikhiln.kudupudi@gmail.com' ,'bik');

select login('knihiw','hh');

## Function 3
## To get total cart value 

delimiter $$
create function cart_total_charge(id int)
returns int 
deterministic 
begin 
	declare cart_total int;
    
	select sum(c.Quantity * b.price) into cart_total
	from cart c
	join book b on b.ISBN = c.ISBN
	where c.Customer_ID = id
	group by c.Customer_ID;
    
    return cart_total;
    
end $$
delimiter ;

select cart_total_charge(1);

select *,cart_total_charge(ID)
from customer;

select * from customer;

select * from book where ISBN = '0030096189';


### Procedure to increase the cart value by one 
# Increasing elements in cart 

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

call inc_qty(1,'0002005018');
select * from cart;

### Procedure to decrease the quantity by 1 of book
# Increasing or decreasing elements in cart 

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

call dec_qty(1,'0002005018');
select @val;
select * from cart;


## 7th Procedure
# procedure to delete row from cart (removing product from cart)
# tried function but not giving proper output 

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

insert into cart values(1,'0002005018',4);
select * from cart;

call delete_book_cart(1,'0002005018',@val);
select @val;

select * from cart;

delete from cart 
where Customer_ID = 5;

### View's 

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

select * from some_view
where title = 'Clara Callan';

select * from store
where zipcode = '02130';

## 8th Procedure 
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
