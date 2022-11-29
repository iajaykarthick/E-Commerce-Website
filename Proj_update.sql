#CREATE USER 'devuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'idmp';
use book_store;

drop table book;
drop table Publisher;


create table ZipCode(
Zip_Code char(7) primary key ,
City varchar(20) not null,
State varchar(20) not null,
Country varchar(20) not null
);

create table Publisher(
Publisher_ID int primary key auto_increment,
Publisher_Name varchar(20) not null,
Publisher_Email varchar(15) not null,
Publisher_Office_Address varchar(30) not null,
Zip_Code char(7) not null,
FOREIGN KEY (Zip_Code) REFERENCES ZipCode(Zip_Code)

);


create table Book(
ISBN varchar(10) primary key unique,
Book_Name varchar(25) not null,
Price float not null,
Published_Year year,
Publisher_ID int,
FOREIGN KEY (Publisher_ID) REFERENCES Publisher(Publisher_ID)
);


create table Author(
Author_ID int primary key auto_increment,
Author_Name varchar(20) not null,
Author_Email varchar(15) not null,
Author_Address varchar(30) not null,
Zip_Code char(7) not null,
FOREIGN KEY (Zip_Code) REFERENCES ZipCode(Zip_Code)
);

create table Author_Book(
Author_ID int  ,
ISBN varchar(10)  ,
primary key(Author_ID,ISBN),
FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

create table Store(
Store_ID int primary key auto_increment,
Store_Address varchar(30) not null,
Zip_Code char(7) not null,
FOREIGN KEY (Zip_Code) REFERENCES ZipCode(Zip_Code)
);

create table Store_Copies(
Store_ID int ,
ISBN varchar(10)  ,
Number_Of_Copies int,
primary key(Store_ID,ISBN),
FOREIGN KEY (Store_ID) REFERENCES Store(Store_ID),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);


create table Subscription(
Subscription_ID int primary key,
Subscription_Type varchar(10),
Subscription_Price float,
Subscription_Duration time
);



create table Customer(
Customer_ID int primary key auto_increment,
Customer_First_Name varchar(20) not null,
Customer_Last_Name varchar(20) not null,
Customer_Email varchar(15) not null,
Customer_Gender varchar(5) not null,
Customer_Address varchar(30) not null,
Customer_Phone char(11) not null,
Zip_Code char(7) not null,
Subscription_ID int not null,
Subscription_Start_Date date not null,
Subscription_End_Date date not null,
FOREIGN KEY (Zip_Code) REFERENCES ZipCode(Zip_Code),
FOREIGN KEY (Subscription_ID) REFERENCES Subscription(Subscription_ID)
);


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

create table Genre(
Genre_ID int auto_increment primary key,
Genre varchar(20)
);

create table Book_Genre(
Genre_ID int ,
ISBN varchar(10),
primary key(Genre_ID,ISBN),
FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

create table Customer_Preference(
Customer_ID int,
Genre_ID int ,
primary key(Customer_ID,Genre_ID),
FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID)
);




