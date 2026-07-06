from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ProductForm
from .models import Product
from accounts.models import Profile


def get_profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile


@login_required
def seller_dashboard(request):
    profile = get_profile(request.user)

    if profile.role != 'Seller':
        messages.error(request, "Only sellers can access dashboard")
        return redirect('home')

    if profile.is_approved == False:
        messages.error(request, "Your seller account is not approved yet")
        return redirect('home')

    return render(request, 'seller_dashboard.html')


@login_required
def add_product(request):
    profile = get_profile(request.user)

    if profile.role != 'Seller':
        messages.error(request, "Only sellers can add products")
        return redirect('home')

    if profile.is_approved == False:
        messages.error(request, "Your seller account is not approved yet")
        return redirect('home')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.status = 'Pending'
            product.save()

            messages.success(request, "Product submitted for admin approval")
            return redirect('seller_dashboard')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


@login_required
def my_products(request):
    profile = get_profile(request.user)

    if profile.role != 'Seller':
        messages.error(request, "Only sellers can view products")
        return redirect('home')

    if profile.is_approved == False:
        messages.error(request, "Your seller account is not approved yet")
        return redirect('home')

    products = Product.objects.filter(seller=request.user)
    return render(request, 'my_products.html', {'products': products})


@login_required
def update_product(request, product_id):
    profile = get_profile(request.user)

    if profile.role != 'Seller':
        messages.error(request, "Only sellers can update products")
        return redirect('home')

    if profile.is_approved == False:
        messages.error(request, "Your seller account is not approved yet")
        return redirect('home')

    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            updated_product = form.save(commit=False)
            updated_product.status = 'Pending'
            updated_product.save()

            messages.success(request, "Product updated and sent for admin approval")
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'update_product.html', {'form': form})


@login_required
def delete_product(request, product_id):
    profile = get_profile(request.user)

    if profile.role != 'Seller':
        messages.error(request, "Only sellers can delete products")
        return redirect('home')

    if profile.is_approved == False:
        messages.error(request, "Your seller account is not approved yet")
        return redirect('home')

    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()

    messages.success(request, "Product deleted successfully")
    return redirect('my_products')

def products_page(request):
    
    products = Product.objects.filter(status='Approved')
    
    return render(
        request,
        'products.html',
        {'products': products}
    )
    
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id, status='Approved')
    
    return render(
        request,
        'Product_detail.html',
        {'product': product}
    )

           
        
    
