from rest_framework.test import APITestCase
from django.urls import reverse 
from rest_framework import status
from products.models import Product
from leads.models import Lead
from order.models import Order
from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch


class TelegramWebhookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("telegram-webhook")

    @patch("messaging.views.webhook.send_telegram_message")
    @patch("messaging.views.webhook.handle_message")
    def test_message_flow(self, mock_handle_message, mock_send):
        """
        Test: normal message goes to handle_message
        """
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
        mock_handle_message.assert_called_once_with("/start", 123)
        mock_send.assert_called_once()
    @patch("messaging.views.webhook.send_telegram_message")
    @patch("messaging.views.webhook.handle_callback")
    @patch("messaging.views.webhook.requests.post")
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