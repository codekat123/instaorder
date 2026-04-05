from rest_framework.decorators import api_view
from rest_framework.response import Response 
from ..services import handle_message
import requests
import json
import os 


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
    requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": text
        }
    )

@api_view(["POST"])
def telegram_webhook(request):
    data = request.data  

    message_data = data.get("message")
    if not message_data:
        return Response({"status": "ignored"})

    message = message_data.get("text", "")
    sender_id = message_data.get("chat", {}).get("id")

    reply = handle_message(message, sender_id)

    send_telegram_message(sender_id, reply)

    return Response({"status": "ok"})