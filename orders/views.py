from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from products.models import Product 

@login_required
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id, status='Approved')
    
    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        payment_method = request.POST.get('payment_method')
        
        Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=product.price * quantity,
            payment_method=payment_method,
            status='Pending'
            
        ) 
        
        return redirect('order_success')
    return render(request, 'checkout.html', {'product': product})

@login_required
def order_success(request):
    return render(request, 'order_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'my_orders.html', {'orders': orders})