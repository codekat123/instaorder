from bot.services import handle_callback, handle_message
from bot.models import Conversation
from rest_framework.test import APITestCase
from django.urls import reverse 
from rest_framework import status
from ..models import Product
from ..models import Lead
from ..models import Order
from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch


class TelegramWebhookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("telegram-webhook")

    @patch("bot.views.webhook.send_telegram_message")
    @patch("bot.views.webhook.handle_message")
    def test_message_flow(self, mock_handle_message, mock_send):

        mock_handle_message.return_value = {
            "text": "Hello",
            "reply_markup": None
        }

        payload = {
            "message": {
                "text": "/start",
                "chat": {"id": 123}
            }
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 200)
        mock_handle_message.assert_called_once_with("/start", 123, None)
        mock_send.assert_called_once()
    @patch("bot.views.webhook.send_telegram_message")
    @patch("bot.views.webhook.handle_callback")
    @patch("bot.views.webhook.requests.post")
    def test_callback_flow(self, mock_requests, mock_handle_callback, mock_send):
        mock_handle_callback.return_value = {
            "text": "Done",
            "reply_markup": None
        }

        payload = {
            "callback_query": {
                "id": "abc",
                "from": {"id": 123},
                "data": "confirm_order"
            }
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 200)
        mock_handle_callback.assert_called_once_with("confirm_order", 123)
        args, kwargs = mock_requests.call_args
        self.assertIn("answerCallbackQuery", args[0])
        self.assertEqual(kwargs["json"], {"callback_query_id": "abc"})
        mock_send.assert_called_once()

    def test_ignore_invalid(self):
        """
        Test: empty payload is ignored
        """
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ignored")

def test_create_order(self):
    lead = Lead.objects.create(external_id="123")
    product = Product.objects.create(name="iPhone", price=1000)



    handle_callback(f"order_{product.id}", "123")


    contact = {
        "user_id": 123,
        "phone_number": "+123456789"
    }

    handle_message(None, "123", contact)


    order = Order.objects.filter(lead=lead).first()

    self.assertIsNotNone(order)
    self.assertEqual(order.product, product)
    self.assertEqual(order.status, "pending")

    def test_confirm_order(self):
        lead = Lead.objects.create(external_id="123")
        product = Product.objects.create(name="iPhone", price=1000)

        order = Order.objects.create(
            lead=lead,
            product=product,
            status="pending"
        )

        response = handle_callback(f"confirm_{order.id}", "123")

        order.refresh_from_db()

        self.assertEqual(order.status, "confirmed")
    
    def test_cancel_order(self):
        lead = Lead.objects.create(external_id="123")
        product = Product.objects.create(name="iPhone", price=1000)

        order = Order.objects.create(
            lead=lead,
            product=product,
            status="pending"
        )



        response = handle_callback(f"cancel_{order.id}", "123")

        self.assertFalse(Order.objects.filter(id=order.id).exists())