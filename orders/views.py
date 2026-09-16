from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Order
from products.models import Product


@login_required
def checkout(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        status="Approved"
    )

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()

        house_number = request.POST.get("house_number", "").strip()
        street = request.POST.get("street", "").strip()
        landmark = request.POST.get("landmark", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        pincode = request.POST.get("pincode", "").strip()
        country = request.POST.get("country", "India").strip()

        payment_method = request.POST.get(
            "payment_method",
            "COD"
        )

        quantity_value = request.POST.get(
            "quantity",
            "1"
        )

        try:
            quantity = int(quantity_value)

        except ValueError:
            quantity = 1

        if quantity < 1:
            quantity = 1

        if not full_name:
            messages.error(
                request,
                "Please enter your full name."
            )

        elif not phone:
            messages.error(
                request,
                "Please enter your phone number."
            )

        elif not email:
            messages.error(
                request,
                "Please enter your email address."
            )

        elif not house_number:
            messages.error(
                request,
                "Please enter your house or flat number."
            )

        elif not street:
            messages.error(
                request,
                "Please enter your street or area."
            )

        elif not city:
            messages.error(
                request,
                "Please enter your city."
            )

        elif not state:
            messages.error(
                request,
                "Please enter your state."
            )

        elif not pincode:
            messages.error(
                request,
                "Please enter your pincode."
            )

        elif payment_method not in ["COD", "ONLINE"]:
            messages.error(
                request,
                "Please select a valid payment method."
            )

        else:

            total_price = product.price * quantity

            order = Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                total_price=total_price,

                full_name=full_name,
                phone=phone,
                email=email,

                house_number=house_number,
                street=street,
                landmark=landmark,
                city=city,
                state=state,
                pincode=pincode,
                country=country,

                payment_method=payment_method,
                status="Pending"
            )

            return redirect(
                "order_success",
                order_id=order.id
            )

    context = {
        "product": product
    }

    return render(
        request,
        "checkout.html",
        context
    )


@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    context = {
        "order": order
    }

    return render(
        request,
        "order_success.html",
        context
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    context = {
        "orders": orders
    }

    return render(
        request,
        "my_orders.html",
        context
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    context = {
        "order": order
    }

    return render(
        request,
        "order_detail.html",
        context
    )


@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status in ["Pending", "Confirmed"]:

        order.status = "Cancelled"
        order.save()

        messages.success(
            request,
            "Your order has been cancelled successfully."
        )

    else:

        messages.error(
            request,
            "This order cannot be cancelled now."
        )

    return redirect(
        "order_detail",
        order_id=order.id
    )