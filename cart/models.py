from django.db import models
from products.models import Product
from users.models import CustomUser

class Cart(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='cart')

    def __str__(self):
        return f"Cart of {self.user}"

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    class Meta:
        unique_together=('cart','product')

    def __str__(self):
        return f"{self.product.title}"
