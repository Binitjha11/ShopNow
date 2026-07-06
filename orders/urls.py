from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
]