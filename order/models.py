from django.db import models
from leads.models import Lead
from products.models import Product


class OrderChoice(models.TextChoices):
    PENDING = 'pending' , 'Pending'
    CONFIRMED = 'confired' , 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'

class Order(models.Model):
    
    lead = models.ForeignKey(
        Lead,   
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=200,
        choices=OrderChoice.choices,
        default=OrderChoice.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return f"{self.lead} - {self.lead}"