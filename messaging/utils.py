from difflib import get_close_matches
from products.models import Product
import requests
import os


def find_product(message):
    name = [p.name.lower() for p in Product.objects.all()]
    match = get_close_matches(message,name,n=1,cutoff=0.5)

    if match:
        return Product.objects.get(name__iexact=match[0])
    return None


def send_telegram_message(chat_id, text,reply_markup=None):
    url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup
    
    requests.post(url,json=payload)


