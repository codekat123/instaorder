from leads.models import Lead
from .handle_callback import handle_callback


def handle_message(message: str, sender_id: str):
    lead, _ = Lead.objects.get_or_create(external_id=sender_id)

    if message == "/start":
        buttons = {
            "inline_keyboard": [
                [{"text": "📦 View Products", "callback_data": "view_products"}],
                [{"text": "📄 My Orders", "callback_data": "view_orders"}],
            ]
        }

        return {
            "text": "Welcome to InstaOrder 🚀",
            "reply_markup": buttons
        }

    if message == "/status":
        return handle_callback("view_orders", sender_id)

    return {
        "text": "Use /start to begin 🙂"
    }