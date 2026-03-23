from products.models import Product
from order.models import Order
from leads.models import Lead


def handle_message(message: str, sender_id: str):
    message = message.lower()

   
    lead, _ = Lead.objects.get_or_create(external_id=sender_id)


    if message.strip() == "yes":
        order = Order.objects.filter(
            lead=lead,
            status="pending"
        ).last()

        if order:
            order.status = "confirmed"
            order.save()
            return f"Order confirmed for {order.product.name} ✅"
        else:
            return "No pending order found."

    if "price" in message or "how much" in message:
        intent = "get_price"
    elif "buy" in message or "order" in message:
        intent = "create_order"
    else:
        intent = "unknown"


    product = None
    for p in Product.objects.filter(is_active=True):
        if p.name.lower() in message:
            product = p
            break


    if intent == "get_price":
        if product:
            return f"The price of {product.name} is {product.price}"
        else:
            return "Which product do you mean?"

    # 🔹 Handle order creation
    if intent == "create_order":
        if product:
            Order.objects.create(
                lead=lead,
                product=product,
                status="pending"
            )
            return f"Order created for {product.name}. Reply YES to confirm."
        else:
            return "Which product do you want to order?"

    return "Sorry, I didn't understand."