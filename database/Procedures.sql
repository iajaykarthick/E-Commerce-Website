## 1 Stored Procedure 
# Getting book name with author 

delimiter $$
create procedure books_with_author(
	in author_name varchar(80) 
)
begin 
	select a.Author_Name, ab.ISBN, b.title
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
	select p.Publisher_Name,b.ISBN,b.title
	from book b 
	join publisher p on p.Publisher_ID = b.Publisher_ID
	where p.Publisher_Name like concat('%',publisher_name,'%');

end $$
delimiter ;

## 3rd Procedure
# Getting book name with Genre  
delimiter $$
create procedure books_with_genre(
	in genre_name varchar(80) 
)
begin 
	select g.genre, b.ISBN, b.title 
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

select * 
from book
where Published_Year = '2001';

delimiter $$
create procedure books_with_year(
	in year_value varchar(80) 
)
begin 
	select ISBN,title
	from book
	where Published_Year = year_value;
    
end $$
delimiter ;

call books_with_year(2001);


