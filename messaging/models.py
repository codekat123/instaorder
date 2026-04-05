from django.db import models
from leads.models import Lead
from products.models import Product




class Conversation(models.Model):
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE)
    current_product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    current_intent = models.CharField(max_length=50,null=True)
    updated_at = models.DateTimeField(auto_now=True)