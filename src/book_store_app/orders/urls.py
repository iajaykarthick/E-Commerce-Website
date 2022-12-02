from django.urls import path, re_path
from . import views

app_name = 'orders'

urlpatterns = [
    path('confirmation/', views.confirmation, name='confirmation'),
    path('list/', views.view_orders, name='view_orders'),
]