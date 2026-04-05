from rest_framework.test import APITestCase
from django.urls import reverse 
from rest_framework import status
from products.models import Product
from leads.models import Lead
from order.models import Order



class WebhookTests(APITestCase):
    def setUp(self):
        self.url = reverse('meta-webhook')
        self.product = Product.objects.create(name="Test Product", price=9.99)
        self.sender_id = "test_sender_123"

    def test_price_inquiry(self):
        response = self.client.post(self.url, {"message": "What's the price of Test Product?", "sender_id": self.sender_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("The price of Test Product is 9.99", response.data['reply'])

    def test_order_creation_and_confirmation(self):

        response = self.client.post(self.url, {"message": "I want to buy Test Product", "sender_id": self.sender_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Order created for Test Product. Reply YES to confirm.", response.data['reply'])

 
        response = self.client.post(self.url, {"message": "YES", "sender_id": self.sender_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Order confirmed for Test Product ✅", response.data['reply'])
    
    def test_unknown_message(self):
        
        response = self.client.post(self.url,{"message":"random message","sender_id":self.sender_id}, format='json')

        self.assertIn('Sorry',response.data['reply'])

    def test_product_not_found(self):
        response = self.client.post(self.url, {
            "message": "price of something else",
            "sender_id": self.sender_id
        }, format='json')

        self.assertIn("Which product", response.data['reply'])
    
    def test_confirm_without_order(self):
        response = self.client.post(self.url, {
            "message": "YES",
            "sender_id": self.sender_id
        }, format='json')

        self.assertIn("No pending order", response.data['reply'])