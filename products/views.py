from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Category, Product


def user_is_seller(user):

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    try:
        return (
            user.profile.role.lower() == "seller"
            and user.profile.is_approved
        )

    except AttributeError:
        return False


def products_page(request):

    products = Product.objects.filter(
        status="Approved"
    ).select_related(
        "category",
        "subcategory",
        "seller"
    )

    categories = Category.objects.all()

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    category_id = request.GET.get(
        "category",
        ""
    ).strip()

    if search_query:

        products = products.filter(

            Q(name__icontains=search_query)

            | Q(description__icontains=search_query)

            | Q(category__name__icontains=search_query)

            | Q(subcategory__name__icontains=search_query)
        )

    if category_id:

        try:
            products = products.filter(
                category_id=int(category_id)
            )

        except ValueError:
            category_id = ""

    products = products.order_by(
        "-id"
    )

    paginator = Paginator(
        products,
        12
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {
        "page_obj": page_obj,
        "products": page_obj,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_id,
    }

    return render(
        request,
        "products.html",
        context
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product.objects.select_related(
            "category",
            "subcategory",
            "seller"
        ),
        id=product_id,
        status="Approved"
    )

    related_products = Product.objects.filter(
        category=product.category,
        status="Approved"
    ).exclude(
        id=product.id
    ).order_by(
        "-id"
    )[:4]

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(
        request,
        "product_detail.html",
        context
    )


@login_required
def seller_dashboard(request):

    if not user_is_seller(
        request.user
    ):

        messages.error(
            request,
            "Only approved sellers can access "
            "the seller dashboard."
        )

        return redirect(
            "home"
        )

    products = Product.objects.filter(
        seller=request.user
    ).select_related(
        "category",
        "subcategory"
    ).order_by(
        "-id"
    )

    context = {
        "products": products,

        "total_products": products.count(),

        "approved_products": products.filter(
            status="Approved"
        ).count(),

        "pending_products": products.filter(
            status="Pending"
        ).count(),

        "rejected_products": products.filter(
            status="Rejected"
        ).count(),
    }

    return render(
        request,
        "seller_dashboard.html",
        context
    )


@login_required
def my_products(request):

    if not user_is_seller(
        request.user
    ):

        messages.error(
            request,
            "Only approved sellers can view products."
        )

        return redirect(
            "home"
        )

    products = Product.objects.filter(
        seller=request.user
    ).select_related(
        "category",
        "subcategory"
    ).order_by(
        "-id"
    )

    return render(
        request,
        "my_products.html",
        {
            "products": products
        }
    )


@login_required
def add_product(request):

    if not user_is_seller(
        request.user
    ):

        messages.error(
            request,
            "Only approved sellers can add products."
        )

        return redirect(
            "home"
        )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            product = form.save(
                commit=False
            )

            product.seller = request.user

            product.status = "Pending"

            product.save()

            messages.success(
                request,
                "Product added successfully. "
                "It is waiting for admin approval."
            )

            return redirect(
                "seller_dashboard"
            )

        messages.error(
            request,
            "Please correct the errors shown below."
        )

    else:

        form = ProductForm()

    return render(
        request,
        "add_product.html",
        {
            "form": form
        }
    )


@login_required
def edit_product(request, product_id):

    if not user_is_seller(
        request.user
    ):

        messages.error(
            request,
            "Only approved sellers can edit products."
        )

        return redirect(
            "home"
        )

    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            updated_product = form.save(
                commit=False
            )

            updated_product.seller = request.user

            updated_product.status = "Pending"

            updated_product.save()

            messages.success(
                request,
                "Product updated successfully. "
                "It has been sent again for approval."
            )

            return redirect(
                "seller_dashboard"
            )

        messages.error(
            request,
            "Please correct the errors shown below."
        )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "update_product.html",
        {
            "form": form,
            "product": product
        }
    )


@login_required
def delete_product(request, product_id):

    if not user_is_seller(
        request.user
    ):

        messages.error(
            request,
            "Only approved sellers can delete products."
        )

        return redirect(
            "home"
        )

    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )

    if request.method == "POST":

        product_name = product.name

        product.delete()

        messages.success(
            request,
            f"{product_name} deleted successfully."
        )

        return redirect(
            "seller_dashboard"
        )

    return render(
        request,
        "delete_product.html",
        {
            "product": product
        }
    )