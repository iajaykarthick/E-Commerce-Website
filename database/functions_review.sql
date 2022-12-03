
# Function 1 
# Function to check the quantity of cart 
DROP FUNCTION IF EXISTS cart_total_qty;
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

-- select cart_total_qty(18);


## Function 2
## Function to check login 
DROP FUNCTION IF EXISTS login;
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
    
-- select login('nikhiln.kudupudi@gmail.com' ,'bik');

-- select login('knihiw','hh');

## Function 3
## To get total cart value 
DROP FUNCTION IF EXISTS cart_total_charge;
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

-- select cart_total_charge(1);

-- select *,cart_total_charge(ID)
-- from customer;

-- select * from customer;

-- select * from book where ISBN = '0030096189';



## Function 4
## To get total cart value 

## input will ISBN, store_id, no of copies 

delimiter $$
create function check_copies_present(sid int, 
book_isbn varchar(10),
ncopies int)

returns int 
deterministic 
begin 
	declare copies_present int;
    
	select count(*) into copies_present
	from store_copies
	where Store_ID = sid and ISBN = book_isbn and Number_Of_Copies >= ncopies;
    
    return copies_present;
    
end $$
delimiter ;