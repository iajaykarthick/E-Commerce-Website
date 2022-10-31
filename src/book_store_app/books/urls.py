from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$',views.book_list,name='list'),
    # path('', views.book_list, name='books_list'),
    # path('login', views.login, name='login'),
]