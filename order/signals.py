from django.db.models.signals import post_save 
from django.dispatch import receiver
from .models import Order 
from messaging.utils import send_telegram_message
import os

@receiver(post_save, sender=Order)
def notify_admin_order(order):
    buttons = {
        "inline_keyboard": [
            [
                {
                    "text": "✅ Confirm",
                    "callback_data": f"admin_confirm_{order.id}"
                },
                {
                    "text": "🚚 Ship",
                    "callback_data": f"admin_ship_{order.id}"
                },
                {
                    "text": "❌ Cancel",
                    "callback_data": f"admin_cancel_{order.id}"
                }
            ]
        ]
    }

    send_telegram_message(
        os.getenv("ADMIN_CHAT_ID"),
        f"🛒 *New Order*\n\n"
        f"👤 User: `{order.lead.external_id}`\n"
        f"📦 Product: *{order.product.name}*\n"
        f"📌 Status: {order.status}",
        reply_markup=buttons
    )