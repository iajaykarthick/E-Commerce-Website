from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.redirect_view, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register')
    # path('book-list/', views.showAll, name='book-list'),
    # path('book-detail/<int:id>/', views.viewBook, name='book-detail'),
    # path('book-create/', views.addBook, name='book-create'),
    # path('test/', views.sp_get, name='test'),
    
    
    # path('home/', views.home, name='home'),
    
]