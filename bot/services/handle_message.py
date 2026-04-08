from ..models import Lead , Conversation 
from .handle_callback import handle_callback
from .orders import handle_phone_submission


def handle_message(message: str, sender_id: str,contact=None):

    lead, _ = Lead.objects.get_or_create(external_id=sender_id)
    conversation, _ = Conversation.objects.get_or_create(lead=lead)

    if contact and conversation.current_intent == "awaiting_phone":
        return handle_phone_submission(contact, sender_id, conversation, lead)

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