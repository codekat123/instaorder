from django.db.models.signals import post_save 
from django.dispatch import receiver
from .models import Order 
from bot.utils import send_telegram_message
import os


@receiver(post_save, sender=Order)
def notify_admin_order(sender, instance, created, **kwargs):
    buttons = {
        "inline_keyboard": [
            [
                {
                    "text": "✅ Confirm",
                    "callback_data": f"admin_confirm_{instance.id}"
                },
                {
                    "text": "🚚 Ship",
                    "callback_data": f"admin_ship_{instance.id}"
                },
                {
                    "text": "❌ Cancel",
                    "callback_data": f"admin_cancel_{instance.id}"
                }
            ]
        ]
    }

    send_telegram_message(
        os.getenv("ADMIN_CHAT_ID"),
        f"🛒 *New instance*\n\n"
        f"👤 User: `{instance.lead.external_id}`\n"
        f"📦 Product: *{instance.product.name}*\n"
        f"📌 Status: {instance.status}",
        reply_markup=buttons
    )