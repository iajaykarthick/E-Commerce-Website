from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import time
from . import db



def home(request):
    return HttpResponse('<h1>Hello World!</h1>')

def redirect_view(request):
    
    response = redirect('accounts:login')
    return response

def register_user(request):
    
    context = {'error_msg': ''}
    if request.method == 'POST':
        print(f'Request is {request.POST}')
            

        ## Insert into customer table 
        print(type(request.POST['password']))
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
    if request.method == 'POST':
        print(f'Request is {request.POST["email"]}')
        print(f'Request is {request.POST["password"]}')
        
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        
        if db.check_if_user_is_valid(email, pwd):
            request.session['user_id'] = email
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