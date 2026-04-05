from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def create_product_link(sender, instance, created, **kwargs):
    if created:

        instance.link = f"https://t.me/codekat_bot?start=product_{instance.id}"
        instance.save()