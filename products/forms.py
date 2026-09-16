from django import forms

from .models import Product, ProductImage, SubCategory


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [
            "category",
            "subcategory",
            "name",
            "price",
            "description",
            "image",
        ]

        widgets = {

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "subcategory": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product name"
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product price",
                    "min": "1"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product description",
                    "rows": 5
                }
            ),

            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs
        )

        self.fields["subcategory"].queryset = (
            SubCategory.objects
            .select_related("category")
            .order_by(
                "category__name",
                "name"
            )
        )

        self.fields["subcategory"].required = False

    def clean(self):

        cleaned_data = super().clean()

        category = cleaned_data.get(
            "category"
        )

        subcategory = cleaned_data.get(
            "subcategory"
        )

        if (
            category
            and subcategory
            and subcategory.category_id != category.id
        ):

            self.add_error(
                "subcategory",
                "Selected subcategory does not belong "
                "to the selected category."
            )

        return cleaned_data


class ProductImageForm(forms.ModelForm):

    class Meta:

        model = ProductImage

        fields = [
            "image"
        ]

        widgets = {

            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            )
        }