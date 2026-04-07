from ..models import Order, Product, Conversation , OrderChoice, Lead
from django.shortcuts import get_object_or_404

def handle_order_start(product_id, lead_id):
        product = get_object_or_404(Product,id=product_id)
        lead = Lead.objects.get_or_create(external_id=lead_id)[0]
        conversation, _= Conversation.objects.get_or_create(lead=lead)
        conversation.current_intent = "awaiting_phone"
        conversation.current_product = product
        conversation.save()

        keyboard = {
            "keyboard": [
                [
                    {
                        "text": "📞 Share Phone Number",
                        "request_contact": True
                    }
                ]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }

        return {
            "text": f"📞 Please share your phone number to order *{product.name}*",
            "reply_markup": keyboard
        }


def handle_confirm(order_id, lead_id):
    try:
        order = Order.objects.get(id=order_id, lead__external_id=lead_id, status="pending")
        order.status = OrderChoice.CONFIRMED
        order.save()

        return {
            "text": f"Order confirmed for {order.product.name} ✅"
        }
    except Order.DoesNotExist:
        return {"text": "No pending order found."}


def handle_cancel(order_id,lead_id):
     try:
        order = Order.objects.get(id=order_id, lead__external_id=lead_id, status="pending")
        order.delete()
        return {"text": "Order cancelled ❌"}
     except Order.DoesNotExist:
        return {"text": "No pending order found to cancel."}
     


def handle_view_orders(lead):
    orders = Order.objects.filter(lead=lead).order_by("-created_at")

    if not orders.exists():
        return {"text": "You have no orders yet."}

    text = "Your Orders:\n"
    for order in orders:
        text += f"- {order.product.name}: {order.status}\n"

    return {"text": text}

def handle_phone_submission(contact, sender_id, conversation, lead):
    if contact.get("user_id") != int(sender_id):
        return {"text": "❌ Please share your own phone number"}
    if not conversation.current_product:
        return {"text": "❌ No product selected. Start again."}
    phone = contact.get("phone_number")

    order = Order.objects.create(
        lead=lead,
        product=conversation.current_product,
        status="pending",
        phone_number=phone
    )


    conversation.current_intent = None
    conversation.current_product = None
    conversation.save()

    return {
        "text": f"Order created for {order.product.name}. Confirm?",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "✅ Confirm", "callback_data": f"confirm_{order.id}"},
                    {"text": "❌ Cancel", "callback_data": f"cancel_{order.id}"}
                ]
            ]
        }
    }