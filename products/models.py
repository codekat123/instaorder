from django.db import models



class Product(models.Model):

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    link = models.URLField(null=True,editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

