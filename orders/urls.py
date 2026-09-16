from django.urls import path
from . import views

urlpatterns = [

    path(
        "checkout/<int:product_id>/",
        views.checkout,
        name="checkout"
    ),

    path(
        "order-success/<int:order_id>/",
        views.order_success,
        name="order_success"
    ),

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    path(
        "order/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

    path(
        "cancel-order/<int:order_id>/",
        views.cancel_order,
        name="cancel_order"
    ),

]