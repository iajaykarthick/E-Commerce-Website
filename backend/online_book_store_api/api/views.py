from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.db import connection


from .serializers import BookSerializer, ResultSerializer
from .models import Book

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/book-list/',
        'Detail View': '/book-detail/<int:id>',
        'Create': '/book-create',
        'Update': '/book-update/<int:id>',
        'Delete': '/book-delete/<int:id>',
    }
    
    return Response(api_urls)

@api_view(['GET'])
def showAll(request):
    books = Book.objects.all()
    print(books)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def viewBook(request, id):
    book = Book.objects.get(id=id)
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def addBook(request):
    
    serializer = BookSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)


@api_view(['GET'])
def sp_get(request):
    
    cursor = connection.cursor()
    cursor.execute('call search_id_book("2,4")')
    
    query_results = cursor.fetchall()
    
    columns = [col[0] for col in cursor.description]
    print(columns)
    results = [{col: col_value for col, col_value in zip(columns, row)} for ind, row in enumerate(query_results)]
    print(results)
    
    serializer = ResultSerializer({'result': results}, many=False)
    
    return Response(serializer.data['result'])