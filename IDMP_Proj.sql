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
#### add to cart or update
## input - customer id, ISBN, QTY 
## if present update or create that row


select count(*)
from cart
where customer_id = 1 and ISBN = 0002005018;

desc cart;

delimiter $$
create procedure books_name(
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

end $$
delimiter ;



 
### Functions 

select sum(Quantity) 
from cart
where Customer_ID = 1
group by Customer_ID;

## Add your your customer_id 
insert into cart(Customer_ID, ISBN, Quantity) values(1,'0002005018',1); 
insert into cart(Customer_ID, ISBN, Quantity) values(1,'0020199090',10);

select * from customer;
select * from cart;
select * from book;
desc cart;

# Function 1 
# Function to check the quantity of qart 
delimiter $$ 
create function cart_total(cid int)
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

select cart_total(18);


## Function 1 
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

select login('knihiw','hh')



## Function 2

delimiter $$
create function newcustomer(
fname varchar(20),
lname varchar(20),
email_id varchar(80),
gen varchar(15),
ph char(12),
address varchar(30),
zipcode char(7),
subid int
)
returns varchar(100)
deterministic 
begin 

# checking if email exist's  
	declare login_validity int;
    declare output varchar(100);
    
    select count(*) into login_validity
	from customer
	where customer.Email = email_id;
    
    if login_validity < 1 then
		INSERT INTO CUSTOMER 
		(First_Name, Last_Name, Email, Gender, Phone, Address, Zipcode, Subscription_ID, Subscription_Start_Date) 
		VALUES (fname, lname, email_id, gen, ph, address, zipcode, subid, now());
		set output = 'Account created Successfully';	
        
    else
		set output = 'There was some error creating the account';
    end if;
    
    return output;
    
end $$
delimiter ;

select newcustomer('Nhfffh', 'Kgggd', 'nikhiln.kudupudi@gmail.com', 'male', '546-697-8889', '445 dat', '02130', '2');
select newcustomer('Nhfffh', 'Kgggd', 'nikka@yaho.com', 'male', '546-697-8889', '445 dat', '02130', '2');
select newcustomer('gggg','fsdsdf','@gmail','male', '540-657-9989', '445 dat', '02130', '2');
select newcustomer('nikhi','kudu','knikhilrao@gmail.com','male', '857-445-9989', '126 day', '02130', '3');

select * from customer;
desc customer;

### 3rd Function 
# Increasing or decreasing elements in cart 

delimiter $$
create function inc_qty(cid int,book_isbn char(10))
returns varchar(100)
deterministic 
begin 
	declare no_of_copies int;
    declare add_copies int;
    declare note varchar(100);
    
	select Quantity into no_of_copies
	from cart
	where Customer_ID = cid;
    
	set add_copies = no_of_copies + 1;
	UPDATE cart
	SET Quantity = add_copies
	WHERE Customer_ID = cid ;
	set note = 'Increased by 1';
    
    return note;
    
end $$
delimiter ;

select inc_qty(1,'0002005018');

### 4th Function 
# Increasing or decreasing elements in cart 

delimiter $$
create function dec_qty(cid int,book_isbn char(10))
returns varchar(100)
deterministic 
begin 
	declare no_of_copies int;
    declare remove_copies int;
    declare note varchar(100);
    
	select Quantity into no_of_copies
	from cart
	where Customer_ID = cid;
    
	set remove_copies = no_of_copies - 1;
	UPDATE cart
	SET Quantity = remove_copies
	WHERE Customer_ID = cid ;
	set note = 'Descreased by 1';
    
    return note;
    
end $$
delimiter ;

select dec_qty(1,'0002005018');

select * from cart;



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
    
    

