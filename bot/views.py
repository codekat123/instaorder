from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import (
    handle_message,
    handle_callback,
    answer_callback,
    send_telegram_message,
    is_rate_limited
)
import logging
import requests
logger = logging.getLogger(__name__)




@api_view(["POST"])
def telegram_webhook(request):
    data = request.data

    logger.info(f"Incoming webhook: {data}")

    try:
        if "callback_query" in data:
            callback = data["callback_query"]

            sender_id = callback["from"]["id"]
            
            if is_rate_limited(sender_id):
                return Response({"status": "rate_limited"})
            
            callback_data = callback["data"]
            callback_id = callback["id"]

            logger.info(f"Callback from {sender_id}: {callback_data}")

            reply = handle_callback(callback_data, sender_id)

            answer_callback(callback_id)

            if reply:
                send_telegram_message(
                    sender_id,
                    reply["text"],
                    reply.get("reply_markup")
                )

            return Response({"status": "ok"})



        message_data = data.get("message")
        if not message_data:
            logger.warning("No message or callback in request")
            return Response({"status": "ignored"})

        message = message_data.get("text")
        contact = message_data.get("contact")
        sender_id = message_data.get("chat", {}).get("id")

        logger.info(f"Message from {sender_id}: {message} | contact={bool(contact)}")

        reply = handle_message(message, sender_id, contact)

        if reply:
            send_telegram_message(
                sender_id,
                reply["text"],
                reply.get("reply_markup")
            )

        return Response({"status": "ok"})

    except Exception as e:
        logger.error(f"Webhook crashed: {e}", exc_info=True)
        return Response({"status": "error"})