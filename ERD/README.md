Overall Description of the Proposed System

1.	Customer:
a.	The customer has ID as a primary key which is system generated.
b.	The customer has an email that will be unique and will be used for logging in.
c.	The customer has a first name, last name, gender, phone, and address.
d.	The zip code is a foreign key, and each customer will have a single zip code.
e.	The subscription id is a foreign key, and each customer can choose a plan for the subscription. There will be a start date and end date for the subscription.

2.	Subscription
a.	Each customer must subscribe to a plan.
b.	The plans will be basic, silver, gold, and platinum.
c.	Better plans can give faster delivery, discounts, and other benefits.
d.	The price and duration of applicability are stored for each subscription.
e.	A customer can upgrade the subscription as per need. 	

3.	Zip code
a.	Zip code is a primary key and each customer will have a single zip code.
b.	Each zip code has an associated state and country.
c.	The customer can update his/her address and zip code.

4.	Login Table
a.	Each customer’s customer_id, password, and the last login time will be stored in the login table.
b.	The password is stored in a different table for safety and for faster access of passwords against the customer id.

5.	Genre
a.	There will be a unique id for each genre and a name for it.

6.	Customer Preference
a.	Each customer can like multiple genres.
b.	The customer can select his/her favorite genres while registering.
c.	The genres can be deleted, or new likings can be added.
d.	The primary key for the table is both Genre_ID and Customer_ID.

7.	Book
a.	Each book is uniquely identified by the ISBN which is the primary key.
b.	Each book has a name, price, and published year.
c.	The publisher_id is a foreign key to tell which publisher has published that book.


8.	Publisher.
a.	Each publisher has an ID that will uniquely identify that publisher and is the primary key.
b.	Each publisher has a name e-mail and office address.
c.	The zip code will be the foreign key from the zip code table.


9.	Author
a.	Each author has an author ID which is the primary key.
b.	The author has a name e-mail ID and address.
c.	The zip code is a foreign key that refers to the zip code table.

10.	Author Book
a.	One book can have multiple authors also one author can have multiple books hence the author_book table is created to store the relation.
b.	the author book table has the author ID and the book ISBN as the primary key.

11.	Wish List
a.	A wish list is a table where the customer can store the books, he/she wants to buy later.
b.	The customer can get a notification if there is a certain discount applied to the books which are there in the wish list. The
c.	the wish list has the customer ID and the book ISBN as the primary keys, and they are also the foreign keys to the customer and the book table.

12.	Cart

a.	The customers can add books to a cart and then after clicking on proceed he/she can pay for the books.
b.	In the cart table, we store the ISBN and the customer id which are the primary keys and the foreign keys to customer and book. 
c.	It is an intermediate table as one customer can add many books to cart and one book can be added by multiple customers.

13.	Order
a.	The order ID uniquely identifies each order.
b.	A customer can place multiple orders on different days.
c.	Each order will have a total price.
d.	The customer chooses a payment type which is denoted by payment ID which refers to the payment table.

14.	Order Items
a.	One order can have many books also one book can belong to multiple orders.
b.	Hence order-items are an intermediatory table that stores this relation.
c.	Each book can be ordered in multiple quantities. The number_of_copies store this relation.
d.	To view the order of a customer we aggregate the order items table with the order table.

15.	Store
a.	The bookstore has multiple branches, and each store is identified by the ID which is the primary key.
b.	each store has an address and a zip code which is the foreign key and refers to the zip code table.

16.	Store Copies
a.	Each store has multiple books, and one book can belong to multiple stores hence store copies are an intermediary table to keep this relation.
b.	the store copy will have the store ID and the book ISBN as the primary keys and they're also the foreign keys that refer to the store and the book.
c.	it will also store the number of copies of each book that the store has.
d.	the number of copies will be dynamically updated once the customer buys books from that store.
e.	only an admin will be able to add new copies to a particular store.
