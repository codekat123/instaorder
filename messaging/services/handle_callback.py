from leads.models import Lead
from products.models import Product
from order.models import Order

def handle_callback(callback_data: str, sender_id: str):
    lead, _ = Lead.objects.get_or_create(external_id=sender_id)


    if callback_data == "view_products":
        products = Product.objects.all()

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

    if callback_data.startswith("product_"):
        product_id = int(callback_data.split("_")[1])
        product = Product.objects.get(id=product_id)

        buttons = {
            "inline_keyboard": [
                [
                    {"text": "💰 Price", "callback_data": f"price_{product.id}"},
                    {"text": "🛒 Order", "callback_data": f"order_{product.id}"}
                ],
                [{"text": "⬅️ Back", "callback_data": "view_products"}]
            ]
        }

        return {
            "text": f"{product.name}",
            "reply_markup": buttons
        }


    if callback_data.startswith("price_"):
        product_id = int(callback_data.split("_")[1])
        product = Product.objects.get(id=product_id)

        return {
            "text": f"The price of {product.name} is {product.price} 💰"
        }


    if callback_data.startswith("order_"):
        product_id = int(callback_data.split("_")[1])
        product = Product.objects.get(id=product_id)

        Order.objects.create(
            lead=lead,
            product=product,
            status="pending"
        )

        buttons = {
            "inline_keyboard": [
                [
                    {"text": "✅ Confirm", "callback_data": "confirm_order"},
                    {"text": "❌ Cancel", "callback_data": "cancel_order"}
                ]
            ]
        }

        return {
            "text": f"Order created for {product.name}. Confirm?",
            "reply_markup": buttons
        }

  
    if callback_data == "confirm_order":
        order = Order.objects.filter(lead=lead, status="pending").last()

        if order:
            order.status = "confirmed"
            order.save()

            return {
                "text": f"Order confirmed for {order.product.name} ✅"
            }

        return {"text": "No pending order found."}


    if callback_data == "cancel_order":
        order = Order.objects.filter(lead=lead, status="pending").last()

        if order:
            order.delete()

        return {"text": "Order cancelled ❌"}

    
    if callback_data == "view_orders":
        orders = Order.objects.filter(lead=lead).order_by("-created_at")

        if not orders.exists():
            return {"text": "You have no orders yet."}

        text = "Your Orders:\n"
        for order in orders:
            text += f"- {order.product.name}: {order.status}\n"

        return {"text": text}

    return {"text": "Something went wrong 😅"}