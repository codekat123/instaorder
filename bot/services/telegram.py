import logging
import requests
import os


logger = logging.getLogger(__name__)



def answer_callback(callback_id):
    try:
        requests.post(
            f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/answerCallbackQuery",
            json={"callback_query_id": callback_id},
            timeout=5
        )
    except Exception as e:
        logger.error(f"Failed to answer callback: {e}")


def send_telegram_message(chat_id, text, reply_markup=None, retries=2):
    for attempt in range(retries):
        try:
            url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"

            payload = {
                "chat_id": chat_id,
                "text": text,
            }

            if reply_markup:
                payload["reply_markup"] = reply_markup

            requests.post(url, json=payload)
            return
        except Exception as e:
            logger.warning(f"Send failed (attempt {attempt+1}): {e}")
    
    logger.error(f"Failed to send message to {chat_id} after retries")


