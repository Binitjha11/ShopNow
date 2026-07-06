from django.urls import path
from . import views

urlpatterns = [
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('my-products/', views.my_products, name='my_products'),
    path('update-product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/', views.products_page, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
]