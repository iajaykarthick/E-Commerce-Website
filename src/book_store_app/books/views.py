from django.http import HttpResponse
from django.shortcuts import render
from .models import Book

# Create your views here.

app_name = 'books'

def book_list(request):
    books = Book.objects.all()
    print(books)
    return render(request,'books/books_list.html',{'books':books})
    #return HttpResponse('<h1>Books List </h1>')
    # 