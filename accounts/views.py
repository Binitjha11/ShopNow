from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Profile
from products.models import Product
from orders.models import Order


def home(request):
    products = Product.objects.filter(status='Approved')[:8]
    return render(request, 'home.html', {'products': products})


def signup_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)

        Profile.objects.create(user=user, role=role)

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'signup.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid username or password")
        return redirect('login')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('home')


def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    context = {
        'total_users': User.objects.count(),
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'pending_products': Product.objects.filter(status='Pending').count(),
    }

    return render(request, 'admin_dashboard.html', context)


def pending_products(request):
    if not request.user.is_superuser:
        return redirect('home')

    products = Product.objects.filter(status='Pending')
    return render(request, 'pending_products.html', {'products': products})


def approve_product(request, product_id):
    if not request.user.is_superuser:
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    product.status = 'Approved'
    product.save()

    return redirect('pending_products')


def reject_product(request, product_id):
    if not request.user.is_superuser:
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    product.status = 'Rejected'
    product.save()

    return redirect('pending_products')
def manage_orders(request):
    if not request.user.is_superuser:
        return redirect('home')

    orders = Order.objects.all().order_by('-created_at')

    paginator = Paginator(orders, 10)   # Show 10 orders per page

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'manage_orders.html', {
        'page_obj': page_obj
    })

def update_order_status(request, order_id, status):
    if not request.user.is_superuser:
        return redirect('home')
    
    order = Order.objects.get(id=order_id)
    order.status = status 
    order.save()
    
    return redirect('manage_orders')

def pending_sellers(request):
    if not request.user.is_superuser:
        return redirect('home')

    sellers = Profile.objects.filter(role='Seller', is_approved=False)

    return render(request, 'pending_sellers.html', {'sellers': sellers})


def approve_seller(request, profile_id):
    if not request.user.is_superuser:
        return redirect('home')

    seller = Profile.objects.get(id=profile_id)
    seller.is_approved = True
    seller.save()

    return redirect('pending_sellers')



