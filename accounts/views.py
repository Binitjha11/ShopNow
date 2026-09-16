from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from orders.models import Order
from products.models import Product

from .models import Profile


def home(request):

    products = Product.objects.filter(
        status="Approved"
    ).order_by(
        "-id"
    )[:8]

    return render(
        request,
        "home.html",
        {
            "products": products
        }
    )


def signup_page(request):

    if request.user.is_authenticated:

        return redirect(
            "home"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        role = request.POST.get(
            "role",
            "Customer"
        )

        if not username:

            messages.error(
                request,
                "Username is required."
            )

            return redirect(
                "signup"
            )

        if not email:

            messages.error(
                request,
                "Email is required."
            )

            return redirect(
                "signup"
            )

        if User.objects.filter(
            username__iexact=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect(
                "signup"
            )

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "Email already registered."
            )

            return redirect(
                "signup"
            )

        if len(password) < 6:

            messages.error(
                request,
                "Password must contain at least 6 characters."
            )

            return redirect(
                "signup"
            )

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect(
                "signup"
            )

        if role not in [
            "Customer",
            "Seller"
        ]:

            role = "Customer"

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user,
            role=role,
            is_approved=(
                role == "Customer"
            )
        )

        if role == "Seller":

            messages.success(
                request,
                "Seller account created successfully. "
                "Please wait for admin approval."
            )

        else:

            messages.success(
                request,
                "Account created successfully. "
                "You can now log in."
            )

        return redirect(
            "login"
        )

    return render(
        request,
        "signup.html"
    )


def login_page(request):

    if request.user.is_authenticated:

        return redirect(
            "home"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        if not username or not password:

            messages.error(
                request,
                "Username and password are required."
            )

            return redirect(
                "login"
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect(
                "login"
            )

        login(
            request,
            user
        )

        if user.is_superuser:

            messages.success(
                request,
                f"Welcome back, {user.username}."
            )

            return redirect(
                "admin_dashboard"
            )

        try:

            profile = user.profile

        except Profile.DoesNotExist:

            profile = Profile.objects.create(
                user=user,
                role="Customer",
                is_approved=True
            )

        if (
            profile.role == "Seller"
            and not profile.is_approved
        ):

            logout(
                request
            )

            messages.warning(
                request,
                "Your seller account is waiting "
                "for admin approval."
            )

            return redirect(
                "login"
            )

        next_url = request.POST.get(
            "next"
        ) or request.GET.get(
            "next"
        )

        if (
            next_url
            and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={
                    request.get_host()
                },
                require_https=request.is_secure()
            )
        ):

            return redirect(
                next_url
            )

        messages.success(
            request,
            f"Welcome back, {user.username}."
        )

        if (
            profile.role == "Seller"
            and profile.is_approved
        ):

            return redirect(
                "seller_dashboard"
            )

        return redirect(
            "home"
        )

    return render(
        request,
        "login.html",
        {
            "next": request.GET.get(
                "next",
                ""
            )
        }
    )


def logout_page(request):

    logout(
        request
    )

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect(
        "home"
    )


@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect(
            "home"
        )

    context = {
        "total_users": User.objects.count(),

        "total_products": Product.objects.count(),

        "total_orders": Order.objects.count(),

        "pending_products": Product.objects.filter(
            status="Pending"
        ).count(),

        "pending_sellers": Profile.objects.filter(
            role="Seller",
            is_approved=False
        ).count(),
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )


@login_required
def pending_products(request):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect(
            "home"
        )

    products = Product.objects.filter(
        status="Pending"
    ).select_related(
        "category",
        "subcategory",
        "seller"
    ).order_by(
        "-id"
    )

    return render(
        request,
        "pending_products.html",
        {
            "products": products
        }
    )


@login_required
def approve_product(
    request,
    product_id
):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect(
            "home"
        )

    product = get_object_or_404(
        Product,
        id=product_id
    )

    product.status = "Approved"

    product.save()

    messages.success(
        request,
        f"{product.name} approved successfully."
    )

    return redirect(
        "pending_products"
    )


@login_required
def reject_product(
    request,
    product_id
):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect(
            "home"
        )

    product = get_object_or_404(
        Product,
        id=product_id
    )

    product.status = "Rejected"

    product.save()

    messages.warning(
        request,
        f"{product.name} rejected."
    )

    return redirect(
        "pending_products"
    )


@login_required
def pending_sellers(request):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect(
            "home"
        )

    sellers = Profile.objects.filter(
        role="Seller",
        is_approved=False
    ).select_related(
        "user"
    ).order_by(
        "user__username"
    )

    return render(
        request,
        "pending_sellers.html",
        {
            "sellers": sellers
        }
    )


@login_required
def approve_seller(
    request,
    profile_id
):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect(
            "home"
        )

    seller = get_object_or_404(
        Profile,
        id=profile_id,
        role="Seller"
    )

    seller.is_approved = True

    seller.save()

    messages.success(
        request,
        f"{seller.user.username} approved as seller."
    )

    return redirect(
        "pending_sellers"
    )


@login_required
def manage_orders(request):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect(
            "home"
        )

    orders = Order.objects.select_related(
        "user",
        "product"
    ).order_by(
        "-created_at"
    )

    paginator = Paginator(
        orders,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        "manage_orders.html",
        {
            "page_obj": page_obj,
            "orders": page_obj
        }
    )


@login_required
def update_order_status(
    request,
    order_id,
    status
):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect(
            "home"
        )

    valid_statuses = [
        "Pending",
        "Accepted",
        "Delivered",
        "Cancelled"
    ]

    if status not in valid_statuses:

        messages.error(
            request,
            "Invalid order status."
        )

        return redirect(
            "manage_orders"
        )

    order = get_object_or_404(
        Order,
        id=order_id
    )

    order.status = status

    order.save()

    messages.success(
        request,
        f"Order status updated to {status}."
    )

    return redirect(
        "manage_orders"
    )