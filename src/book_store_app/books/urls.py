from django.urls import path, re_path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='list'),
    path('book-detail/<slug:isbn>/', views.book_detail, name='detail'),
    path('add-to-cart/', views.get_cart_details, name='cart'),
    # re_path(r'^(?P<slug>[\w-]+)/$', views.book_detail, name='detail'),
    # path('', views.book_list, name='books_list'),
    # path('login', views.login, name='login'),

]