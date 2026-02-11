from django.db import models
from products.models import Product
from users.models import CustomUser
from decimal import Decimal



class Order(models.Model):
    STATUS_NEW = "new"
    STATUS_PAID = "paid"
    STATUS_SHIPPED = "shipped"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (STATUS_NEW, "New"),
        (STATUS_PAID, "Paid"),
        (STATUS_SHIPPED, "Shipped"),
        (STATUS_CANCELLED, "Cancelled"),
    )
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='orders')
    status=models.CharField(max_length=30,choices=STATUS_CHOICES,default=STATUS_NEW)
    total_price=models.DecimalField(max_digits=12,decimal_places=2,default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product} x {self.quantity}"





