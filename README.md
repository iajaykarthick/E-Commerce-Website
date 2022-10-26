# Online-Book-Store

To run the application locally, clone the repository and run below commands inside local repo directory

```
cd backend/online_book_store_api
python manage.py runserver
```
Application will be live at http://127.0.0.1:8000/

To install django,
```
conda install -c ananconda django
```


#### Testing api 
Below APIs created so far:

#### Get book data based on book id 

http://localhost:8000/api/book-detail/2/

#### Get all data from book table

http://localhost:8000/api/book-list

#### Call sample stored procedure

http://localhost:8000/api/test


#### Initial ERD
![ERD](ERD/Book_Store_ERD.jpg)