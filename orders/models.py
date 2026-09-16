from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Order(models.Model):

    PAYMENT_CHOICES = [
        ("COD", "Cash On Delivery"),
        ("ONLINE", "Online Payment"),
    ]

    ORDER_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Packed", "Packed"),
        ("Shipped", "Shipped"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    quantity = models.PositiveIntegerField(default=1)

    total_price = models.IntegerField()

    full_name = models.CharField(
        max_length=100,
        default=""
    )

    phone = models.CharField(
        max_length=15,
        default=""
    )

    email = models.EmailField(
        default=""
    )

    house_number = models.CharField(
        max_length=100,
        default=""
    )

    street = models.CharField(
        max_length=200,
        default=""
    )

    landmark = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    city = models.CharField(
        max_length=100,
        default=""
    )

    state = models.CharField(
        max_length=100,
        default=""
    )

    pincode = models.CharField(
        max_length=10,
        default=""
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="COD"
    )

    status = models.CharField(
        max_length=30,
        choices=ORDER_STATUS_CHOICES,
        default="Pending"
    )

    courier_partner = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    current_location = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    estimated_delivery = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"

    def complete_address(self):
        address_parts = [
            self.house_number,
            self.street,
            self.landmark,
            self.city,
            self.state,
            self.pincode,
            self.country,
        ]

        return ", ".join(
            part for part in address_parts if part
        )