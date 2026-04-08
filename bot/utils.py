from difflib import get_close_matches
from .models import Product



def find_product(message):
    name = [p.name.lower() for p in Product.objects.all()]
    match = get_close_matches(message,name,n=1,cutoff=0.5)

    if match:
        return Product.objects.get(name__iexact=match[0])
    return None


