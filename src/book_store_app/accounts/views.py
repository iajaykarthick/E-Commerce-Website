from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import time
from . import db

from books import db as books_db

# login required
from book_store_app.decorators import admin_login_required

def redirect_view(request):
    response = redirect('accounts:login')
    return response

def register_user(request):
    
    context = {'error_msg': ''}
    if request.method == 'POST':
        customer_id = db.insert_customer(request.POST["fname"],
                           request.POST["lname"],
                           request.POST["email"],
                           request.POST["gender"],
                           request.POST["phone"],
                           request.POST["address"],
                           request.POST["zipcode"],
                           request.POST["subscription"],
                           time.strftime('%Y-%m-%d %H:%M:%S')
                           )
        
        if customer_id > 0:
            db.insert_login_info(customer_id, request.POST['password'])
            return redirect('accounts:login')
        else:
            context['error_msg'] = 'User creation failed - Invalid data entered'
            print('error occurred')

    return render(request, 'accounts/register.html', context)

def login_user(request):
    context = {'error_msg': ''}
    
    if 'user_id' in request.session:
        return redirect('books:list')
    
    if request.method == 'POST':
        print(f'Request is {request.POST["email"]}')
        print(f'Request is {request.POST["password"]}')
        
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        
        if email == 'admin@bookstore' and pwd == 'admin':
            user_id = 'admin'
            request.session['user_id'] = user_id
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('accounts:admin-page')
        
        elif db.check_if_user_is_valid(email, pwd):
            user_id = db.get_customer_id(email)
            if user_id != -1:
                request.session['user_id'] = user_id
            
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('books:list')
        
        else:
            context['error_msg'] = 'Incorrect Email Address / Password'
        
    return render(request,'accounts/login.html', context)

def logout_user(request):
    del request.session['user_id']
    response = redirect('accounts:login')
    return response


@admin_login_required
def admin_page(request):
    result = books_db.get_user_types()
    context={}
    temp1=[]
    temp2=[]
    titles=[]
    sold_count=[]
    dates=[]
    sales=[]
    month=[]
    monthly_sales=[]
    genre=[]
    book_count=[]
    store_id=[]
    copies_sold=[]
    for i in result:
        temp1.append(i[0])
        temp2.append(i[1])
    result = books_db.get_top_sold_books()
    for i in result:
        titles.append(i[0])
        sold_count.append(i[1])
    result=books_db.get_sale_last_5_days()
    for i in result:
        dates.append(str(i[0]))
        sales.append(i[1])
    result=books_db.monthly_rev()
    for i in result:
        month.append(str(i[0]))
        monthly_sales.append(i[1])

    result=books_db.popular_genre()
    for i in result:
        genre.append(i[0])
        book_count.append(i[1])


    result = books_db.store_best_performing()
    for i in result:
        store_id.append(i[0])
        copies_sold.append(i[1])


    context['ids']=temp1
    context['count']=temp2
    context['titles']=titles
    context['sold_count']=sold_count
    context['dates']=dates
    context['sales']=sales
    context['month']=month
    context['monthly_sales']=monthly_sales
    context['genre']=genre
    context['book_count']=book_count
    context['store_id']=store_id
    context['copies_sold']=copies_sold
    print(context)
    return render(request, 'accounts/admin.html', context)





