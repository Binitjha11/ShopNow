from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('pending-products/', views.pending_products, name='pending_products'),
    path('approve-product/<int:product_id>/', views.approve_product, name='approve_product'),
    path('reject-product/<int:product_id>/', views.reject_product, name='reject_product'),
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    
    
    path(
        'update-order-status/<int:order_id>/<str:status>/',
        views.update_order_status,
        name='update_order_status'
        ),
    
    path('pending-sellers/', views.pending_sellers, name='pending_sellers'),
    path('approve-seller/<int:profile_id>/', views.approve_seller, name='approve_seller'),
    
    
    
    
    
]
