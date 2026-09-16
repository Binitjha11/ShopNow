from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductImage,
    SubCategory,
)


class ProductImageInline(admin.TabularInline):

    model = ProductImage

    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "category__name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "seller",
        "category",
        "subcategory",
        "price",
        "status",
    )

    list_filter = (
        "status",
        "category",
        "subcategory",
    )

    search_fields = (
        "name",
        "seller__username",
        "category__name",
        "subcategory__name",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "seller",
    )

    inlines = [
        ProductImageInline
    ]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
    )

    search_fields = (
        "product__name",
    )