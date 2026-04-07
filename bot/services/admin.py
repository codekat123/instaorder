from ..models import Order , OrderChoice
from django.shortcuts import get_object_or_404 

def handle_admin_action(action, order_id):
    order = get_object_or_404(Order, id=order_id)

    status_map = {
        "confirm": OrderChoice.CONFIRMED,
        "ship": OrderChoice.SHIPPED,
        "cancel": OrderChoice.CANCELLED
    }

    if action in status_map:
        order.status = status_map[action]
        order.save()
    else:
        return {"text": "Invalid admin action."}

    return {
        "text": f"Order {order.id} updated to {order.status} ✅"
    }