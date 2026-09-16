from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    ROLE_CHOICES = (
        ("Customer", "Customer"),
        ("Seller", "Seller"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="Customer"
    )

    is_approved = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    
