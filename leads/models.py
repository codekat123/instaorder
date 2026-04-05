from django.db import models
from products.models import Product

class Lead(models.Model):

    external_id = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.external_id
