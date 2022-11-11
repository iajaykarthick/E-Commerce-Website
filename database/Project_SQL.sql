CREATE USER 'devuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'idmp';
use book_store;

drop table book;
drop table Publisher;
drop table ZipCode;

select * from Book;

create table ZipCode(
zipcode char(7) primary key ,
City varchar(30) not null,
State varchar(20) not null,
Country varchar(20) not null
);

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/zipcode.csv'
into table ZipCode
fields terminated by ','
-- ENCLOSED BY '"'
lines terminated by '\n'
ignore 1 rows;

select * from ZipCode;
select count(*) from Zipcode;

create table Publisher(
Publisher_ID int primary key auto_increment,
Publisher_Name varchar(70) not null,
Publisher_Email varchar(80) not null,
Publisher_Office_Address varchar(30) not null,
zipcode char(7) not null,
FOREIGN KEY (zipcode) REFERENCES ZipCode(zipcode)
);

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Publisher.csv'
into table Publisher
fields terminated by ','
ENCLOSED BY '"'
lines terminated by '\r\n'
ignore 1 rows;

select * from Publisher;

-- insert into publisher(Publisher_Name,Publisher_Email,Publisher_Office_Address,zipcode) values('AAA','AAA.gmail.com','Day st','00501');
-- insert into publisher(Publisher_Name,Publisher_Email,Publisher_Office_Address,zipcode) values('AAA2','AA2A.gmail.com','Day 2st','00501');
-- delete from publisher
-- where Publisher_ID = 336;


create table Book(
ISBN varchar(10) primary key unique,
Book_Name varchar(255) not null,
Price float not null,
Published_Year year,
Publisher_ID int,
FOREIGN KEY (Publisher_ID) REFERENCES Publisher(Publisher_ID)
);
drop table Book;


load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/books.csv'
into table Book
fields terminated by ','
ENCLOSED BY '"'
lines terminated by '\n'
ignore 1 rows;

select * from Book;

create table Author(
Author_ID int primary key auto_increment,
Author_Name varchar(80) not null,
Author_Email varchar(80) not null,
Author_Address varchar(30) not null,
Zipcode char(7) not null,
FOREIGN KEY (Zipcode) REFERENCES ZipCode(Zipcode)
);

drop table Author;

select * from Author;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Authors.csv'
into table Author
fields terminated by ','
ENCLOSED BY '"'
lines terminated by '\r\n'
ignore 1 rows;


create table Author_Book(
Author_ID int  ,
ISBN varchar(10)  ,
primary key(Author_ID,ISBN),
FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

drop table Author_Book;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Author_ISBN.csv'
into table Author_Book
fields terminated by ','
ENCLOSED BY '"'
lines terminated by '\n'
ignore 1 rows;

select * from Author_Book;

create table Store(
Store_ID int primary key auto_increment,
Store_Address varchar(30) not null,
Zipcode char(7) not null,
FOREIGN KEY (Zipcode) REFERENCES ZipCode(Zipcode)
);

drop table store;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/store.csv'
into table store
fields terminated by ','
ENCLOSED BY '"'
lines terminated by '\r\n'
ignore 1 rows;

select * from store;
select count(*) from store;


create table Store_Copies(
Store_ID int ,
ISBN varchar(10)  ,
Number_Of_Copies int,
#primary key(Store_ID,ISBN),
FOREIGN KEY (Store_ID) REFERENCES Store(Store_ID),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

drop table Store_Copies;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Store_Copies.csv'
into table Store_Copies
fields terminated by ','
ENCLOSED BY '"'
lines terminated by '\n'
ignore 1 rows;

select * from Store_Copies;

select count(*) 
from Store_Copies;


create table Subscription(
Subscription_ID int primary key,
Subscription_Type varchar(10),
Subscription_Price float,
Subscription_Duration int
);

drop table Subscription;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/subscription.csv'
into table Subscription
fields terminated by ','
ENCLOSED BY '"'
lines terminated by '\n'
ignore 1 rows;

select * from Subscription;


create table Customer(
Customer_ID int primary key auto_increment,
Customer_First_Name varchar(20) not null,
Customer_Last_Name varchar(20) not null,
Customer_Email varchar(50) not null,
Customer_Gender varchar(15) not null,
Customer_Phone char(12) not null,
Customer_Address varchar(30) not null,
Zipcode char(7) not null,
Subscription_ID int not null,
Subscription_Start_Date date not null,
FOREIGN KEY (Zipcode) REFERENCES ZipCode(Zipcode),
FOREIGN KEY (Subscription_ID) REFERENCES Subscription(Subscription_ID)
);

drop table Customer;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/customer.csv'
into table Customer
fields terminated by ','
ENCLOSED BY '"'
lines terminated by '\n'
ignore 1 rows;


select * from customer;

create table Login_Table(
Customer_ID int primary key,
Password varchar(10),
Last_Login timestamp,
FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
);


create table Payment(
Payment_ID int auto_increment primary key,
Payment_Type varchar(20)
);


create table Orders (
Order_ID int auto_increment primary key,
Customer_ID int not null,
Total_Price float,
Payment_ID int,
FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
FOREIGN KEY (Payment_ID) REFERENCES Payment(Payment_ID)
);


create table Order_Items(
Order_ID int,
ISBN varchar(10) ,
Number_Of_Copies varchar(10),
primary key(Order_ID,ISBN),
FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);


create table Wish_List(
Customer_ID int not null,
ISBN varchar(10) ,
primary key(Customer_ID,ISBN),
FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);


create table Cart(
Customer_ID int,
ISBN varchar(10) ,
Quantity int,
primary key(Customer_ID,ISBN),
FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

### Work from here 

create table Genre(
Genre_ID int auto_increment primary key,
Genre varchar(25)
);

drop table Genre;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Genre.csv'
into table Genre
fields terminated by ','
ENCLOSED BY '"'
lines terminated by '\n'
ignore 1 rows;

select * from Genre;

create table Book_Genre(
Genre_ID int ,
ISBN varchar(10),
primary key(Genre_ID,ISBN),
FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

desc Book_Genre;

drop table Book_Genre;


load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/fff.csv'
into table Book_Genre
fields terminated by ','
optionally ENCLOSED BY "'"
lines terminated by '\r'
ignore 1 rows;

select * from Book_Genre;

create table Customer_Preference(
Customer_ID int,
Genre_ID int ,
primary key(Customer_ID,Genre_ID),
FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID)
);




