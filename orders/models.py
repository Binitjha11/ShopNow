from django.db import models
from django.contrib.auth.models import User
from products.models import Product 

class Order(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    quantity = models.IntegerField(default=1)
    
    total_price = models.IntegerField()
    
    payment_method = models.CharField(
        max_length=20,
        choices=[
          ('COD', 'Cash On Delivery'),
          ('ONLINE', 'Online Payment')
          
        ]
    )
    
    status = models.CharField(
        max_length=20,
        default='Pending'
        
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
        
        