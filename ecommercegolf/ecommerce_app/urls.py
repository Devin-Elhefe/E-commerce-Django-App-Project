
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('order-history/', views.order_history, name='order_history'),
    path('register/', views.register, name='register'),
]




