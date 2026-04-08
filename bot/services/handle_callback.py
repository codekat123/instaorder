from ..models import Lead , Product
from .admin import handle_admin_action
from .products import handle_product_view , handle_product
from .orders import handle_order_start , handle_confirm , handle_cancel , handle_view_orders

def handle_callback(callback_data: str, sender_id: str):
    lead, _ = Lead.objects.get_or_create(external_id=sender_id)


    if callback_data.startswith("admin_"):
        _, action, order_id = callback_data.split("_")
        return handle_admin_action(action, order_id)

    if callback_data == "view_products":
        return handle_product_view()


    if callback_data.startswith("product_"):
        return handle_product(int(callback_data.split("_")[1]))


    if callback_data.startswith("price_"):
        product = Product.objects.get(id=int(callback_data.split("_")[1]))
        return {"text": f"{product.name} costs {product.price} 💰"}


    if callback_data.startswith("order_"):
        product_id = int(callback_data.split("_")[1])
        return handle_order_start(product_id,lead.external_id)


    if callback_data.startswith("confirm_"):
        order_id = int(callback_data.split("_")[1])
        return handle_confirm(order_id,lead.external_id)

    if callback_data.startswith("cancel_"):
        order_id = int(callback_data.split("_")[1])
        return handle_cancel(order_id,lead.external_id)

    
    if callback_data == "view_orders":
        return handle_view_orders(lead)

    return {"text": "Something went wrong 😅"}