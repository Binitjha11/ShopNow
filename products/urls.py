from django.urls import path

from . import views


urlpatterns = [

    path(
        "products/",
        views.products_page,
        name="products"
    ),

    path(
        "product/<int:product_id>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "seller/dashboard/",
        views.seller_dashboard,
        name="seller_dashboard"
    ),

    path(
        "my-products/",
        views.my_products,
        name="my_products"
    ),

    path(
        "seller/product/add/",
        views.add_product,
        name="add_product"
    ),

    path(
        "seller/product/<int:product_id>/edit/",
        views.edit_product,
        name="edit_product"
    ),

    path(
        "seller/product/<int:product_id>/delete/",
        views.delete_product,
        name="delete_product"
    ),

    path(
        "update-product/<int:product_id>/",
        views.edit_product,
        name="update_product"
    ),
]