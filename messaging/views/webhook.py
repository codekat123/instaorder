from rest_framework.decorators import api_view
from rest_framework.response import Response 
from ..services import handle_message , handle_callback
from ..utils import send_telegram_message
import requests
import os 



        

@api_view(["POST"])
def telegram_webhook(request):
    data = request.data  

    if "callback_query" in data:
        callback = data["callback_query"]

        sender_id = callback["from"]["id"]
        callback_data = callback["data"]
        callback_id = callback["id"]

        reply = handle_callback(callback_data, sender_id)


        requests.post(
            f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/answerCallbackQuery",
            json={"callback_query_id": callback_id}
        )

        if reply:
            send_telegram_message(
                sender_id,
                reply["text"],
                reply.get("reply_markup")
            )

        return Response({"status": "ok"})

    message_data = data.get("message")
    if not message_data:
        return Response({"status": "ignored"})

    message = message_data.get("text", "")
    sender_id = message_data.get("chat", {}).get("id")

    reply = handle_message(message, sender_id)

    if reply:
        send_telegram_message(
            sender_id,
            reply["text"],
            reply.get("reply_markup")
        )

    return Response({"status": "ok"})