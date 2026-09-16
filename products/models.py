from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    image = models.ImageField(
        upload_to="category_images/",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    name = models.CharField(
        max_length=100
    )

    image = models.ImageField(
        upload_to="subcategory_images/",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_subcategory_per_category"
            )
        ]

        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Product(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="seller_products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="category_products"
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategory_products"
    )

    name = models.CharField(
        max_length=150
    )

    price = models.PositiveIntegerField()

    description = models.TextField()

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    class Meta:
        ordering = ["-id"]

    def clean(self):

        if (
            self.subcategory
            and self.category
            and self.subcategory.category_id != self.category_id
        ):
            raise ValidationError(
                {
                    "subcategory":
                        "Selected subcategory does not belong "
                        "to the selected category."
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(
            *args,
            **kwargs
        )

    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="extra_images"
    )

    image = models.ImageField(
        upload_to="product_images/"
    )

    def __str__(self):
        return f"Image - {self.product.name}"