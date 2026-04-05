from .utils import find_product
from products.models import Product
from order.models import Order
from leads.models import Lead
from .models import Conversation


def handle_message(message: str, sender_id: str):
    message = message.lower().strip()

    lead, _ = Lead.objects.get_or_create(external_id=sender_id)
    conversation, _ = Conversation.objects.get_or_create(lead=lead)

   
    if message == "yes" and conversation.current_intent == "create_order":
        order = Order.objects.filter(lead=lead, status="pending").last()

        if order:
            order.status = "confirmed"
            order.save()

            conversation.current_intent = None
            conversation.current_product = None
            conversation.save()

            return f"Order confirmed for {order.product.name} ✅"
        return "No pending order found."

    
    if "price" in message or "how much" in message:
        intent = "get_price"
    elif "buy" in message or "order" in message:
        intent = "create_order"
    else:
        intent = "unknown"

    conversation.current_intent = intent


    product = find_product(message)

    if product:
        conversation.current_product = product
    else:
        product = conversation.current_product

    conversation.save()


    if intent == "get_price":
        if product:
            return f"The price of {product.name} is {product.price}"
        return "Which product do you mean?"


    if intent == "create_order":
        if product:
            Order.objects.create(
                lead=lead,
                product=product,
                status="pending"
            )
            return f"Order created for {product.name}. Reply YES to confirm."
        return "Which product do you want to order?"

    return "Sorry, I didn't understand."
