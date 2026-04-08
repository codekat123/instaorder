from bot.models import Lead, Product, Order, Conversation, OrderChoice
from django.test import TestCase
from bot.services.handle_message import handle_message
from bot.services.handle_callback import handle_callback
from bot.services.orders import handle_phone_submission


class CoreBotTest(TestCase):
    def setUp(self):
        self.sender_id = "123456789"
        self.lead = Lead.objects.create(external_id=self.sender_id)
        self.product = Product.objects.create(name="Test Product", price=10.00)

    def test_start_command(self):
        response = handle_message("/start", self.sender_id)
        
        self.assertEqual(response["text"], "Welcome to InstaOrder 🚀")
        self.assertIn("inline_keyboard", response["reply_markup"])

    def test_view_products(self):
        response = handle_callback("view_products", self.sender_id)
        
        self.assertEqual(response["text"], "Choose a product:")
        self.assertIn("reply_markup", response)

    def test_order_flow(self):


        response = handle_callback(f"order_{self.product.id}", self.sender_id)
        self.assertIn("Please share your phone number", response["text"])
        

        conversation = Conversation.objects.get(lead=self.lead)
        self.assertEqual(conversation.current_intent, "awaiting_phone")
        self.assertEqual(conversation.current_product, self.product)
        

        contact = {"user_id": int(self.sender_id), "phone_number": "+1234567890"}
        response = handle_phone_submission(contact, self.sender_id, conversation, self.lead)
        
        self.assertIn("Order created", response["text"])
        self.assertIn("reply_markup", response)
        

        order = Order.objects.get(lead=self.lead, product=self.product)
        self.assertEqual(order.status, OrderChoice.PENDING)
        self.assertEqual(order.phone_number, "+1234567890")
        

        response = handle_callback(f"confirm_{order.id}", self.sender_id)
        self.assertEqual(response["text"], f"Order confirmed for {order.product.name} ✅")
        

        order.refresh_from_db()
        self.assertEqual(order.status, OrderChoice.CONFIRMED)

    def test_order_cancellation(self):


        order = Order.objects.create(lead=self.lead, product=self.product, status=OrderChoice.PENDING)
        

        response = handle_callback(f"cancel_{order.id}", self.sender_id)
        self.assertEqual(response["text"], "Order cancelled ❌")

        self.assertFalse(Order.objects.filter(id=order.id).exists())

    def test_view_orders(self):


        Order.objects.create(lead=self.lead, product=self.product, status=OrderChoice.PENDING)
        
        response = handle_callback("view_orders", self.sender_id)
        self.assertIn("Your Orders:", response["text"])
        self.assertIn(self.product.name, response["text"])

    def test_product_details(self):
        response = handle_callback(f"product_{self.product.id}", self.sender_id)
        
        self.assertEqual(response["text"], self.product.name)
        self.assertIn("reply_markup", response)
        
        keyboard = response["reply_markup"]["inline_keyboard"]
        self.assertEqual(len(keyboard), 2)  

    def test_price_inquiry(self):
        response = handle_callback(f"price_{self.product.id}", self.sender_id)
        
        self.assertIn(self.product.name, response["text"])
        self.assertIn(str(self.product.price), response["text"])

    def test_unknown_message(self):
        response = handle_message("random text", self.sender_id)
        self.assertEqual(response["text"], "Use /start to begin 🙂")

    def test_unknown_callback(self):
        response = handle_callback("unknown_action", self.sender_id)
        self.assertEqual(response["text"],"Something went wrong 😅")
