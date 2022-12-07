from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.redirect_view, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('admin-page', views.admin_page, name='admin-page'),
]