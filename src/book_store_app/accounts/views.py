from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Hello World!</h1>')

def redirect_view(request):
    response = redirect('login')
    return response

def login(request):
    return HttpResponse('<h1> Login page </h1>')