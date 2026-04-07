from ..models import Product
from django.shortcuts import get_object_or_404


def handle_product(product_id):
    product = get_object_or_404(Product, id=product_id)

    return {
        "text": product.name,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "💰 Price", "callback_data": f"price_{product.id}"},
                    {"text": "🛒 Order", "callback_data": f"order_{product.id}"}
                ],
                [{"text": "⬅️ Back", "callback_data": "view_products"}]
            ]
        }
    }

def handle_product_view():
        products = Product.objects.filter(is_active=True)

        keyboard = []
        for product in products:
            keyboard.append([
                {
                    "text": f"{product.name} - {product.price}",
                    "callback_data": f"product_{product.pk}"
                }
            ])

        return {
            "text": "Choose a product:",
            "reply_markup": {"inline_keyboard": keyboard}
        }